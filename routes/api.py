from fastapi import APIRouter

api = APIRouter()

@api.get('/')
async def index():
    return {'message': 'Hello from FastAPI!'}
