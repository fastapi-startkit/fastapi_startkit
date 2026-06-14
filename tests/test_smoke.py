from routes.api import index


async def test_index_returns_hello():
    assert await index() == {"message": "Hello from FastAPI!"}
