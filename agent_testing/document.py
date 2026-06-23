"""POC shim: teach ``fastapi_startkit.ai.Document`` to emit a LangChain block.

``Document`` already ships ``to_anthropic_block()`` / ``to_openai_block()``. This
adds the matching LangChain content block so the same attachment works on the
LangGraph backend. When this graduates from POC, move ``to_langchain_block`` onto
``fastapi_startkit/ai/document.py`` next to the other ``to_*_block`` methods.
"""

from __future__ import annotations

from typing import Any


def to_langchain_block(self) -> dict[str, Any]:
    """Return a LangChain content block for this document.

    Text (or text/* media) is inlined as a labelled text part; everything else
    becomes a base64 ``image``/``file`` block the model reads natively.
    """
    is_text = isinstance(self.content, str) or self.media_type.startswith("text/")
    if is_text:
        text = self.content if isinstance(self.content, str) else self.content.decode("utf-8", "replace")
        return {"type": "text", "text": f"[Document: {self.name}]\n{text}"}
    block_type = "image" if self.media_type.startswith("image/") else "file"
    return {"type": block_type, "base64": self.to_base64(), "mime_type": self.media_type}


def install() -> None:
    """Attach ``to_langchain_block`` to Document if it isn't already present."""
    try:
        from fastapi_startkit.ai import Document
    except Exception:  # pragma: no cover - the [ai] extra may be absent
        return
    if not hasattr(Document, "to_langchain_block"):
        Document.to_langchain_block = to_langchain_block
