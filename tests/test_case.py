from fastapi_startkit.fastapi.testing import HttpTestCase

from agent_testing import Agent


class TestCase(HttpTestCase):
    def get_application(self):
        from bootstrap.application import app

        return app

    async def asyncTearDown(self):
        # Reset any global agent fake so it never leaks into the next test.
        Agent.reset()
        await super().asyncTearDown()
