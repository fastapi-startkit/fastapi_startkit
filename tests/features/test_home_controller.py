from tests.test_case import TestCase


class TestHomeController(TestCase):
    async def test_home(self) -> None:
        response = await self.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello from FastAPI!"}
