from __future__ import annotations

import fnmatch
from typing import Any, Callable

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr

Predicate = Callable[[list[BaseMessage]], bool]


class NoFakeResponse(LookupError):
    """Raised when an agent calls the model but no fake response matches."""


def _as_ai_message(value: Any) -> AIMessage:
    if isinstance(value, AIMessage):
        return value
    if isinstance(value, str):
        return AIMessage(content=value)
    raise TypeError(f"Fake responses must be an AIMessage or str, got {type(value).__name__}")


def _latest_human_text(messages: list[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            content = message.content
            if isinstance(content, list):
                parts = [p if isinstance(p, str) else p.get("text", "") for p in content]
                return " ".join(parts)
            return str(content)
    return ""


def _glob_match(pattern: str, text: str) -> bool:
    pattern, text = pattern.lower(), text.lower()
    if any(ch in pattern for ch in "*?["):
        return fnmatch.fnmatch(text, pattern)
    return pattern in text


def _key_predicate(key: str) -> Predicate:
    """Build a matcher for a mapping key.

    A ``tool:<name>`` key matches the model turn that follows a tool's
    execution (when the last message is that tool's result). Any other key is a
    glob/substring pattern matched against the most recent human message — and
    only on non-tool turns, so prompts and tool follow-ups never collide.
    """
    if key.startswith("tool:"):
        name = key[len("tool:") :]

        def match_tool(messages: list[BaseMessage]) -> bool:
            last = messages[-1]
            return isinstance(last, ToolMessage) and _glob_match(name, last.name or "")

        return match_tool

    def match_human(messages: list[BaseMessage]) -> bool:
        if isinstance(messages[-1], ToolMessage):
            return False
        return _glob_match(key, _latest_human_text(messages))

    return match_human


def _compile(responses: Any) -> tuple[list[tuple[Predicate, AIMessage]], bool]:
    if responses is None:
        # Match every call with an empty response, mirroring Http::fake() with no
        # arguments. An explicit mapping stays strict and raises on no match.
        return [(lambda _messages: True, AIMessage(content=""))], False
    if isinstance(responses, dict):
        return [(_key_predicate(k), _as_ai_message(v)) for k, v in responses.items()], False
    if isinstance(responses, (AIMessage, str)):
        return [(lambda _messages: True, _as_ai_message(responses))], False
    if isinstance(responses, (list, tuple)):
        return [(lambda _messages: True, _as_ai_message(v)) for v in responses], True
    raise TypeError(f"Unsupported fake responses type: {type(responses).__name__}")


class FakeChatModel(BaseChatModel):
    """A chat model that returns canned responses instead of calling an API.

    Pass a mapping of patterns to responses for pattern-based stubbing, or a list
    of responses to return in sequence. It never performs network I/O, so agents
    built on it run fully offline.
    """

    responses: Any = None

    _rules: list[tuple[Predicate, AIMessage]] = PrivateAttr(default_factory=list)
    _sequential: bool = PrivateAttr(default=False)
    _cursor: int = PrivateAttr(default=0)
    _calls: list[list[BaseMessage]] = PrivateAttr(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        self._rules, self._sequential = _compile(self.responses)

    @property
    def _llm_type(self) -> str:
        return "fake-chat-model"

    @property
    def calls(self) -> list[list[BaseMessage]]:
        return self._calls

    @property
    def call_count(self) -> int:
        return len(self._calls)

    def bind_tools(self, tools: Any, **kwargs: Any) -> "FakeChatModel":
        # Tools are irrelevant to a stub; keep the same instance so callers can
        # still read `call_count`/`calls` after the agent binds its tools.
        return self

    def __enter__(self) -> "FakeChatModel":
        from .binding import activate

        activate(self)
        return self

    def __exit__(self, *_exc: Any) -> bool:
        from .binding import deactivate

        deactivate()
        return False

    def _select(self, messages: list[BaseMessage]) -> AIMessage:
        self._calls.append(list(messages))

        if self._sequential:
            if self._cursor >= len(self._rules):
                raise NoFakeResponse(f"FakeChatModel ran out of responses after {self._cursor} call(s)")
            _, response = self._rules[self._cursor]
            self._cursor += 1
            return response.model_copy(deep=True)

        for predicate, response in self._rules:
            if predicate(messages):
                return response.model_copy(deep=True)

        raise NoFakeResponse(f"No fake response matched. Last message: {messages[-1].content!r}")

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        message = self._select(messages)
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        message = self._select(messages)
        return ChatResult(generations=[ChatGeneration(message=message)])
