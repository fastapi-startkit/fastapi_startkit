from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.job_assistant import JobAssistant

api = APIRouter()


@api.get("/")
async def index():
    return {"message": "Hello from FastAPI!"}


class ChatRequest(BaseModel):
    message: str


@api.post("/chat")
async def chat(request: ChatRequest):
    reply = await JobAssistant().reply(request.message)
    return {"reply": reply}
