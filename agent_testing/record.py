from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import messages_from_dict, messages_to_dict
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr

RECORD_MODES = ("auto", "record", "replay")


class CassetteMiss(LookupError):
    """Raised in replay mode when no recorded interaction matches a request."""


def _request_key(messages: list) -> str:
    # Drop per-message ``id``s: the agent runtime assigns a fresh UUID to each
    # message on every run, which would otherwise make an identical request hash
    # differently on replay. Tool-call ids inside the payload are left intact
    # since they are replayed verbatim from the cassette and stay stable.
    data = messages_to_dict(messages)
    for item in data:
        item.get("data", {}).pop("id", None)
    payload = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


class RecordingChatModel(BaseChatModel):
    """VCR-style wrapper around a real chat model.

    On a cassette miss it calls the wrapped model and saves the response; on a hit
    it replays from disk without any network I/O. ``mode`` controls the policy:
    ``auto`` records misses and replays hits, ``record`` always re-records, and
    ``replay`` only replays (raising :class:`CassetteMiss` on an unknown request).
    """

    model: Any
    cassette: str
    mode: str = "auto"

    _store: dict[str, dict] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        if self.mode not in RECORD_MODES:
            raise ValueError(f"mode must be one of {RECORD_MODES}, got {self.mode!r}")
        self._store = self._load()

    @property
    def _llm_type(self) -> str:
        return "recording-chat-model"

    @property
    def interactions(self) -> list[dict]:
        return list(self._store.values())

    def _load(self) -> dict[str, dict]:
        path = Path(self.cassette)
        if not path.exists():
            return {}
        data = json.loads(path.read_text())
        return {item["key"]: item for item in data.get("interactions", [])}

    def _save(self) -> None:
        path = Path(self.cassette)
        path.parent.mkdir(parents=True, exist_ok=True)
        document = {"version": 1, "interactions": list(self._store.values())}
        path.write_text(json.dumps(document, indent=2, sort_keys=True))

    def bind_tools(self, tools: Any, **kwargs: Any) -> "RecordingChatModel":
        return self._clone(self.model.bind_tools(tools, **kwargs))

    def _clone(self, model: Any) -> "RecordingChatModel":
        clone = RecordingChatModel(model=model, cassette=self.cassette, mode=self.mode)
        # Share the in-memory store so recordings made through a tool-bound clone
        # are visible to the original instance and written out once.
        clone._store = self._store
        return clone

    def _replay(self, key: str) -> ChatResult | None:
        hit = self._store.get(key)
        if hit is None or self.mode == "record":
            return None
        message = messages_from_dict([hit["response"]])[0]
        return ChatResult(generations=[ChatGeneration(message=message)])

    def _store_response(self, key: str, messages: list, message: Any) -> None:
        self._store[key] = {
            "key": key,
            "request": messages_to_dict(messages),
            "response": messages_to_dict([message])[0],
        }
        self._save()

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        key = _request_key(messages)
        replayed = self._replay(key)
        if replayed is not None:
            return replayed
        if self.mode == "replay":
            raise CassetteMiss(f"No recorded interaction in {self.cassette} for this request")

        message = self.model.invoke(messages, **({"stop": stop} if stop else {}))
        self._store_response(key, messages, message)
        return ChatResult(generations=[ChatGeneration(message=message)])

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        key = _request_key(messages)
        replayed = self._replay(key)
        if replayed is not None:
            return replayed
        if self.mode == "replay":
            raise CassetteMiss(f"No recorded interaction in {self.cassette} for this request")

        message = await self.model.ainvoke(messages, **({"stop": stop} if stop else {}))
        self._store_response(key, messages, message)
        return ChatResult(generations=[ChatGeneration(message=message)])
