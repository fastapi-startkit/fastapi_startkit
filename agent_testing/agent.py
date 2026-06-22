from __future__ import annotations

from typing import Any

from .fake import FakeChatModel
from .record import RecordingChatModel


class Agent:
    """Entry point for the agent test harness.

    Both helpers return a chat model you hand to ``create_agent(model=...)``, so
    the agent under test runs without ever reaching a real model provider.
    """

    @classmethod
    def fake(cls, responses: Any = None, **kwargs: Any) -> FakeChatModel:
        """Stub the model with pattern- or sequence-based canned responses."""
        return FakeChatModel(responses=responses, **kwargs)

    @classmethod
    def record(cls, model: Any, cassette: str, mode: str = "auto", **kwargs: Any) -> RecordingChatModel:
        """Wrap a real model so responses are recorded once then replayed."""
        return RecordingChatModel(model=model, cassette=cassette, mode=mode, **kwargs)
