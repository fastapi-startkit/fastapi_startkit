from app.agents.job_assistant import JobAssistant
from tests.test_case import TestCase


class TestChatApi(TestCase):
    async def test_suggest_jobs_returns_faked_reply(self):
        # Context-manager form: the binding is swapped in on enter and reset on exit.
        with JobAssistant.fake({"*jobs*": "Here are 3 Python jobs."}) as fake:
            response = await self.post("/chat", data={"message": "suggest me jobs"})

            assert response.status_code == 200
            assert response.json() == {"reply": "Here are 3 Python jobs."}
            fake.assert_prompted("*jobs*")

    @JobAssistant.fake({"*summar*": "Q3 revenue was $1.2M."})
    async def test_decorator_form(self):
        response = await self.post("/chat", data={"message": "summarise the q3 report"})

        assert response.status_code == 200
        assert response.json() == {"reply": "Q3 revenue was $1.2M."}
        JobAssistant.faked().assert_prompted("*summar*")

    async def test_default_fake_yields_empty_reply(self):
        with JobAssistant.fake():
            response = await self.post("/chat", data={"message": "anything"})

        assert response.status_code == 200
        assert response.json() == {"reply": ""}

    async def test_chat_accepts_an_uploaded_file(self):
        with JobAssistant.fake({"*summar*": "Q3 revenue was $1.2M."}) as _:
            response = await self.post(
                "/chat",
                data={"message": "Summarise this report."},
                files={"files": ("q3-report.txt", b"Q3 revenue was $1.2M ...", "text/plain")},
            )

            assert response.status_code == 200
            assert response.json() == {"reply": "Q3 revenue was $1.2M."}
