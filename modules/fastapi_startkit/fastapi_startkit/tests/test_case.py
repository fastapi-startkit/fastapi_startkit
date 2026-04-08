import unittest

from core.environment import LoadEnvironment


class TestCase(unittest.TestCase):
    def setUp(self):
        LoadEnvironment('testing')
        from fastapi.testclient import TestClient
        from main import app
        self.client = TestClient(app)

        if hasattr(self, "startTestRun"):
            self.startTestRun()

    def tearDown(self):
        pass
