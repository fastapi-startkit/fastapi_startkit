from core.tests.database_transaction import DatabaseTransactions
from core.tests.test_case import TestCase


class TestUserCanRegister(TestCase, DatabaseTransactions):
    def test_user_can_register(self):
        response = self.client.post("/register", data={"name": "test", "email": "", "password": ""})
        assert response.status_code == 200
