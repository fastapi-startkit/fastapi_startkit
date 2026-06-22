from langchain_core.messages import AIMessage

from agent_testing import Agent
from tests.test_case import TestCase


class TestChatApi(TestCase):
    async def test_suggest_jobs_returns_faked_reply(self):
        # No model injection: fake once, hit the real endpoint, assert the response.
        Agent.fake({"*jobs*": AIMessage(content="Here are 3 Python jobs.")})

        response = await self.post("/chat", json={"message": "suggest me jobs"})

        assert response.status_code == 200
        assert response.json() == {"reply": "Here are 3 Python jobs."}
        Agent.assert_invoked("*jobs*")

    async def test_default_fake_yields_empty_reply(self):
        Agent.fake()

        response = await self.post("/chat", json={"message": "anything"})

        assert response.status_code == 200
        assert response.json() == {"reply": ""}
