from __future__ import annotations

from typing import Any

# create_agent() turns a model string into a model via init_chat_model(). Swapping
# that single chokepoint lets `Agent.fake()` intercept every agent built afterward
# without touching app code -- the Laravel `Http::fake()` ergonomic for agents.
from langchain.agents import factory as _factory

try:
    from langchain import chat_models as _chat_models
except Exception:  # pragma: no cover - secondary, best-effort patch target
    _chat_models = None

_active: Any = None
_originals: dict[str, Any] = {}


def active() -> Any:
    """Return the currently installed fake model, or ``None``."""
    return _active


def is_faking() -> bool:
    return _active is not None


def _fake_init_chat_model(*_args: Any, **_kwargs: Any) -> Any:
    return _active


def activate(model: Any) -> None:
    """Install ``model`` as the global fake, patching the resolver once."""
    global _active
    if _active is None:
        if not hasattr(_factory, "init_chat_model"):
            raise RuntimeError(
                "agent_testing could not find langchain.agents.factory.init_chat_model; "
                "this LangChain version is not supported by the global fake."
            )
        _originals["factory"] = _factory.init_chat_model
        _factory.init_chat_model = _fake_init_chat_model
        if _chat_models is not None and hasattr(_chat_models, "init_chat_model"):
            _originals["chat_models"] = _chat_models.init_chat_model
            _chat_models.init_chat_model = _fake_init_chat_model
    _active = model


def deactivate() -> None:
    """Remove the global fake and restore the real resolver."""
    global _active
    _active = None
    if "factory" in _originals:
        _factory.init_chat_model = _originals.pop("factory")
    if "chat_models" in _originals and _chat_models is not None:
        _chat_models.init_chat_model = _originals.pop("chat_models")
