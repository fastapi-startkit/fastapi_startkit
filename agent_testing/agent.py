from __future__ import annotations

import fnmatch
import functools
import hashlib
import inspect
import json
import sys
from pathlib import Path
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


class CassetteMiss(LookupError):
    """Raised in replay mode when no recorded reply matches the prompt."""


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


def _result(content: str) -> dict:
    """A minimal agent result, matching the shape real ``prompt()`` returns."""
    return {"messages": [AIMessage(content=content)]}


class _Recorder:
    """Tracks prompt calls so stand-ins share the same assertion helpers."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.attachments: list[list["Document"]] = []

    def _record_call(self, message: str, attachments: list["Document"] | None) -> None:
        self.calls.append(message)
        self.attachments.append(list(attachments or []))

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


class FakeAgent(_Recorder):
    """Stand-in bound by ``Agent.fake()``; answers ``prompt()`` from patterns."""

    def __init__(self, responses: dict[str, Any] | None = None):
        super().__init__()
        self.responses = responses or {}

    async def prompt(self, message: str, attachments: list["Document"] | None = None) -> dict:
        self._record_call(message, attachments)
        if not self.responses:
            return _result("")
        for pattern, reply in self.responses.items():
            if _matches(pattern, message):
                return _result(_reply_text(reply))
        raise NoFakeResponse(f"No fake response matched message: {message!r}")


class RecordingAgent(_Recorder):
    def __init__(self, real: Any, cassette: str | None = None):
        super().__init__()
        self._real = real
        # Resolved lazily from the test name when record() is called without a path.
        self.cassette: Path | None = Path(cassette) if cassette else None

    @staticmethod
    def _key(message: str, attachments: list["Document"] | None) -> str:
        names = [getattr(doc, "name", "") for doc in (attachments or [])]
        payload = json.dumps({"message": message, "attachments": names}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    async def prompt(self, message: str, attachments: list["Document"] | None = None) -> dict:
        self._record_call(message, attachments)
        cassette = self.cassette
        assert cassette is not None, "RecordingAgent has no cassette resolved"
        store = json.loads(cassette.read_text()) if cassette.exists() else {}
        key = self._key(message, attachments)
        if key in store:
            return _result(store[key])
        result = await self._real.prompt(message, attachments=attachments)
        store[key] = result["messages"][-1].content
        cassette.parent.mkdir(parents=True, exist_ok=True)
        cassette.write_text(json.dumps(store, indent=2, sort_keys=True))
        return result


class AgentBinding:
    def __init__(self, agent_cls: type["Agent"], stand_in: Any):
        self._agent_cls = agent_cls
        self._stand_in = stand_in

    def _resolve_cassette(self, filename: str, qualname: str) -> None:
        # A record() with no path names its cassette after the test and drops it
        # in a cassettes/ folder next to the test file.
        stand_in = self._stand_in
        if isinstance(stand_in, RecordingAgent) and stand_in.cassette is None:
            name = qualname.replace(".", "_")
            stand_in.cassette = Path(filename).parent / "cassettes" / f"{name}.json"

    def __enter__(self) -> Any:
        from fastapi_startkit.application import app

        caller = sys._getframe(1).f_code
        self._resolve_cassette(caller.co_filename, caller.co_qualname)
        app().bind(self._agent_cls._key(), self._stand_in)
        return self._stand_in

    def __exit__(self, *_exc: Any) -> bool:
        from fastapi_startkit.application import app

        app().unbind(self._agent_cls._key())
        return False

    def __call__(self, func: Callable) -> Callable:
        self._resolve_cassette(inspect.getfile(func), func.__qualname__)
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
    model: str = "google_genai:gemini-2.5-flash"
    system_prompt: str = ""

    def tools(self) -> list:
        return []

    async def prompt(self, message: str, attachments: list["Document"] | None = None) -> dict:
        agent = create_agent(model=self.model, system_prompt=self.system_prompt, tools=self.tools())
        content = _user_content(message, attachments)
        return await agent.ainvoke({"messages": [{"role": "user", "content": content}]})

    @classmethod
    def _key(cls) -> str:
        return cls.__name__

    @classmethod
    def fake(cls, responses: dict[str, Any] | None = None) -> AgentBinding:
        """Stub this agent for the duration of a ``with`` block or a decorated test."""
        return AgentBinding(cls, FakeAgent(responses))

    @classmethod
    def record(cls, cassette: str | None = None) -> AgentBinding:
        """Hit the API once and record the reply to JSON, then replay it.

        With no path the cassette is named after the test and stored in a
        ``cassettes/`` folder next to the test file.
        """
        return AgentBinding(cls, RecordingAgent(cls(), cassette))

    @classmethod
    def make(cls) -> "Agent":
        from fastapi_startkit.application import app

        container = app()
        if container.has(cls._key()):
            return container.make(cls._key())
        return cls()

    @classmethod
    def bound(cls) -> Any:
        """Return the active stand-in (e.g. to assert on inside a decorated test)."""
        from fastapi_startkit.application import app

        container = app()
        if not container.has(cls._key()):
            raise RuntimeError(f"{cls.__name__} has no active fake/record binding")
        return container.make(cls._key())

    # Backwards-friendly alias for the fake case.
    faked = bound
