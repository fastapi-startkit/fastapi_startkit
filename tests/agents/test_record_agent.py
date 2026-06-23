from app.agents.job_assistant import JobAssistant
from tests.test_case import TestCase


class TestChatRecord(TestCase):
    async def test_suggest_jobs_returns_recorded_reply(self):
        # First run hits the API and records to JSON; later runs replay the cassette.
        with JobAssistant.record() as record:
            response = await self.post("/chat", data={"message": "suggest me jobs"})

            assert response.status_code == 200
            assert response.json() == {"reply": "Here are 3 Python jobs."}
            record.assert_prompted("*jobs*")

    @JobAssistant.record()
    async def test_decorator_form(self):
        response = await self.post("/chat", data={"message": "summarise the q3 report"})

        assert response.status_code == 200
        assert response.json() == {"reply": "Q3 revenue was $1.2M."}
        JobAssistant.faked().assert_prompted("*summar*")
