from __future__ import annotations

import fnmatch
import functools
import inspect
from typing import TYPE_CHECKING, Any, Callable

from langchain.agents import create_agent
from langchain_core.messages import AIMessage

from . import document as _document

if TYPE_CHECKING:
    from fastapi_startkit.ai import Document

# Give Document.to_langchain_block() (POC shim until upstreamed into the framework).
_document.install()


class NoFakeResponse(LookupError):
    """Raised when a faked agent receives a message no pattern matches."""


def _user_content(message: str, attachments: list["Document"] | None) -> Any:
    if not attachments:
        return message
    return [{"type": "text", "text": message}, *(doc.to_langchain_block() for doc in attachments)]


def _matches(pattern: str, message: str) -> bool:
    pattern, message = pattern.lower(), message.lower()
    if any(ch in pattern for ch in "*?["):
        return fnmatch.fnmatch(message, pattern)
    return pattern in message


def _reply_text(reply: Any) -> str:
    return reply.content if isinstance(reply, AIMessage) else str(reply)


class FakeAgent:
    """Stand-in bound by ``Agent.fake()``; answers ``prompt()`` from patterns."""

    def __init__(self, responses: dict[str, Any] | None = None):
        self.responses = responses or {}
        self.calls: list[str] = []
        self.attachments: list[list["Document"]] = []

    async def prompt(self, message: str, attachments: list["Document"] | None = None) -> str:
        self.calls.append(message)
        self.attachments.append(list(attachments or []))
        if not self.responses:
            return ""
        for pattern, reply in self.responses.items():
            if _matches(pattern, message):
                return _reply_text(reply)
        raise NoFakeResponse(f"No fake response matched message: {message!r}")

    @property
    def prompt_count(self) -> int:
        return len(self.calls)

    def assert_prompted(self, pattern: str | None = None) -> None:
        if pattern is None:
            assert self.calls, "Expected the agent to be prompted, but it never was."
            return
        assert any(_matches(pattern, message) for message in self.calls), (
            f"Expected a prompt matching {pattern!r}, but none did. Got: {self.calls!r}"
        )

    def assert_not_prompted(self) -> None:
        assert not self.calls, f"Expected no prompts, but got: {self.calls!r}"


class FakeBinding:
    """Returned by ``Agent.fake()`` — binds the fake on enter and, crucially,
    unbinds it again on exit so the swap never leaks. Works two ways::

        with JobAssistant.fake({"*jobs*": "..."}) as fake:
            ...                                  # auto-reset on block exit

        @JobAssistant.fake({"*jobs*": "..."})    # auto-reset after the test
        async def test_chat(self):
            ...
    """

    def __init__(self, agent_cls: type["Agent"], responses: dict[str, Any] | None):
        self._agent_cls = agent_cls
        self.fake = FakeAgent(responses)

    def __enter__(self) -> FakeAgent:
        from fastapi_startkit.application import app

        app().bind(self._agent_cls._key(), self.fake)
        return self.fake

    def __exit__(self, *_exc: Any) -> bool:
        from fastapi_startkit.application import app

        app().unbind(self._agent_cls._key())
        return False

    def __call__(self, func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                with self:
                    return await func(*args, **kwargs)

            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self:
                return func(*args, **kwargs)

        return wrapper


class Agent:
    """Base class for container-resolved agents, with Laravel-style faking.

    Subclass it, set ``system_prompt``/``tools()``, and resolve it in app code with
    ``YourAgent.make()``. Tests swap in a pattern-based fake via
    ``YourAgent.fake({"*jobs*": "..."})`` -- no model, no network, no injection.
    """

    model: str = "google_genai:gemini-2.5-flash"
    system_prompt: str = ""

    def tools(self) -> list:
        return []

    async def prompt(self, message: str, attachments: list["Document"] | None = None) -> str:
        agent = create_agent(model=self.model, system_prompt=self.system_prompt, tools=self.tools())
        content = _user_content(message, attachments)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": content}]})
        return result["messages"][-1].content

    @classmethod
    def _key(cls) -> str:
        return cls.__name__

    @classmethod
    def fake(cls, responses: dict[str, Any] | None = None) -> FakeBinding:
        """Stub this agent for the duration of a ``with`` block or a decorated test."""
        return FakeBinding(cls, responses)

    @classmethod
    def make(cls) -> "Agent":
        from fastapi_startkit.application import app

        container = app()
        if container.has(cls._key()):
            return container.make(cls._key())
        return cls()

    @classmethod
    def faked(cls) -> FakeAgent:
        """Return the active fake (e.g. to assert on inside a decorated test)."""
        from fastapi_startkit.application import app

        container = app()
        if not container.has(cls._key()):
            raise RuntimeError(f"{cls.__name__}.fake() is not active")
        return container.make(cls._key())
