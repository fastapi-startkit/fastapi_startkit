from fastapi import APIRouter, File, Form, UploadFile
from fastapi_startkit.ai import Document

from app.agents.job_assistant import JobAssistant

api = APIRouter()


@api.get("/")
async def index():
    return {"message": "Hello from FastAPI!"}


async def _to_document(file: UploadFile) -> Document:
    return Document(
        content=await file.read(),
        name=file.filename or "upload",
        media_type=file.content_type or "application/octet-stream",
    )


@api.post("/chat")
async def chat(message: str = Form(...), files: list[UploadFile] | None = File(default=None)):
    attachments = [await _to_document(file) for file in (files or [])]
    reply = await JobAssistant.make().prompt(message, attachments=attachments)
    return {"reply": reply}
