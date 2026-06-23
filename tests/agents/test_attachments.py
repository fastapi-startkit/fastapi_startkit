from fastapi_startkit.ai import Document

from agent_testing.agent import _user_content
from app.agents.job_assistant import JobAssistant
from tests.test_case import TestCase


def test_user_content_without_attachments_is_a_plain_string():
    assert _user_content("hi", None) == "hi"


def test_user_content_inlines_a_text_document():
    doc = Document(content="Q3 revenue was $1.2M.", name="q3-report.txt")

    content = _user_content("Summarise this report.", [doc])

    assert content[0] == {"type": "text", "text": "Summarise this report."}
    assert content[1]["type"] == "text"
    assert "q3-report.txt" in content[1]["text"]
    assert "Q3 revenue was $1.2M." in content[1]["text"]


def test_user_content_encodes_a_binary_document_as_a_file_block():
    doc = Document(content=b"%PDF-1.7 ...", name="q3.pdf", media_type="application/pdf")

    block = _user_content("Summarise", [doc])[1]

    assert block["type"] == "file"
    assert block["mime_type"] == "application/pdf"
    assert block["base64"] == doc.to_base64()


class TestAttachmentsThroughAgent(TestCase):
    async def test_fake_receives_the_attachment(self):
        doc = Document(content="Q3 revenue was $1.2M …", name="q3-report.txt")

        with JobAssistant.fake({"*summar*": "Q3 revenue was $1.2M."}) as fake:
            result = await JobAssistant.make().prompt("Summarise this report.", attachments=[doc])

            assert result["messages"][-1].content == "Q3 revenue was $1.2M."
            assert fake.attachments[0][0].name == "q3-report.txt"
