from __future__ import annotations

from typing import Any

from . import binding
from .fake import FakeChatModel, _glob_match, _latest_human_text
from .record import RecordingChatModel


class Agent:
    """Entry point for the agent test harness, in the spirit of Laravel facades.

    ``Agent.fake()`` installs a global stub so every agent built afterward via
    ``create_agent(model="provider:name")`` runs offline -- no injection, no app
    changes. The returned model is also usable directly and as a context manager
    (which resets the global fake on exit).
    """

    @classmethod
    def fake(cls, responses: Any = None, **kwargs: Any) -> FakeChatModel:
        """Globally stub the model. Pass a pattern mapping, a sequence, or nothing."""
        model = FakeChatModel(responses=responses, **kwargs)
        binding.activate(model)
        return model

    @classmethod
    def reset(cls) -> None:
        """Remove the global fake and restore the real model resolver."""
        binding.deactivate()

    @classmethod
    def record(cls, model: Any, cassette: str, mode: str = "auto", **kwargs: Any) -> RecordingChatModel:
        """Wrap a real model so responses are recorded once then replayed."""
        return RecordingChatModel(model=model, cassette=cassette, mode=mode, **kwargs)

    @classmethod
    def _calls(cls) -> list:
        fake = binding.active()
        if fake is None:
            raise RuntimeError("Agent.fake() has not been called; there is nothing to assert.")
        return fake.calls

    @classmethod
    def assert_invoked(cls, pattern: str | None = None) -> None:
        """Assert the faked model was invoked (optionally matching a prompt pattern)."""
        calls = cls._calls()
        if pattern is None:
            assert calls, "Expected the agent to invoke the model, but it never did."
            return
        assert any(_glob_match(pattern, _latest_human_text(messages)) for messages in calls), (
            f"Expected an agent invocation matching {pattern!r}, but none did."
        )

    @classmethod
    def assert_invoked_count(cls, count: int) -> None:
        actual = len(cls._calls())
        assert actual == count, f"Expected {count} model invocation(s), got {actual}."

    @classmethod
    def assert_nothing_invoked(cls) -> None:
        fake = binding.active()
        actual = len(fake.calls) if fake is not None else 0
        assert actual == 0, f"Expected no model invocations, got {actual}."
