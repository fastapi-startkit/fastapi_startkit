# FastAPI StartKit

FastAPI StartKit is a modular, provider-driven framework for building robust FastAPI applications with minimal boilerplate. That said, it doesn't lock you into FastAPI at all — you can build entirely headless CLI utilities, cron scripts, or background task workers and still get the full suite of infrastructure components: logging, database, configuration, and dependency injection.

[Full Documentation](https://fastapi-startkit.github.io/docs/fastapi.html)

## Quick Start

### 1. Clone the repository
```shell
git clone https://github.com/fastapi-startkit/fastapi_startkit example-app
cd example-app
cp .env.example .env
```

### 2. Install dependencies
```shell
uv sync
```

### 3. Run the application
```shell
uv run python artisan serve
```

## Testing Agents

Agents subclass `agent_testing.Agent`, declare their `system_prompt`/`tools()`, and
are resolved through the service container with `make()`. Tests swap in a
pattern-matched stub with `fake()` — **no real model, no network, no injection**.

### Defining an agent

```python
from agent_testing import Agent
from langchain_core.tools import tool

@tool
def search_jobs(query: str) -> list[dict]:
    """Search the job board."""
    ...

class JobAssistant(Agent):
    system_prompt = "You help users find jobs."

    def tools(self):
        return [search_jobs]
```

Resolve it in app code with `JobAssistant.make()`, which returns the fake when one
is bound and the real agent otherwise:

```python
@api.post("/chat")
async def chat(message: str = Form(...), files: list[UploadFile] | None = File(None)):
    attachments = [await _to_document(f) for f in (files or [])]
    reply = await JobAssistant.make().prompt(message, attachments=attachments)
    return {"reply": reply}
```

### Faking in tests

`Agent.fake()` swaps the agent in the container and **auto-resets the binding** when
the block or test ends. Use it as a context manager or a decorator.

```python
# context-manager form — `as fake` gives you the stub to assert on
async def test_suggest_jobs(self):
    with JobAssistant.fake({"*jobs*": "Here are 3 Python jobs."}) as fake:
        response = await self.post("/chat", data={"message": "suggest me jobs"})
        assert response.json() == {"reply": "Here are 3 Python jobs."}
        fake.assert_prompted("*jobs*")

# decorator form — binding resets automatically after the test
@JobAssistant.fake({"*summar*": "Q3 revenue was $1.2M."})
async def test_summary(self):
    response = await self.post("/chat", data={"message": "summarise the q3 report"})
    assert response.json() == {"reply": "Q3 revenue was $1.2M."}
    JobAssistant.faked().assert_prompted("*summar*")
```

Keys are glob/substring patterns matched against the prompt; pass nothing
(`JobAssistant.fake()`) to answer every call with an empty reply. Assertions:
`fake.assert_prompted(pattern=None)`, `fake.assert_not_prompted()`, `fake.prompt_count`.

### Attachments

`prompt()` accepts `attachments=[Document(...)]`. Each document is rendered as a
LangChain content block via `Document.to_langchain_block()` (text is inlined; images
and files become base64 blocks), so multimodal prompts work on the LangGraph backend.

```python
from fastapi_startkit.ai import Document

doc = Document(content="Q3 revenue was $1.2M …", name="q3-report.txt")
reply = await JobAssistant.make().prompt("Summarise this report.", attachments=[doc])
```

### Record & replay (VCR)

`Agent.record(cassette)` uses the same auto-resetting binding, but VCR-style: the
first call hits the real agent and saves the reply to `cassette`; later calls replay
from disk with no network I/O. `mode="replay"` fails on an un-recorded prompt;
`mode="record"` refreshes the cassette.

```python
with JobAssistant.record("tests/cassettes/chat.json"):
    response = await self.post("/chat", data={"message": "suggest me jobs"})
    assert response.status_code == 200
```

Commit the cassette and CI replays it offline. In tests you can pass `real=<stub>`
to record deterministically without hitting the live model.

## AI Skills

Skills teach AI agents (Claude Code, Gemini) this project's conventions.

List providers that declare skills:

```shell
uv run python artisan ai:skills
```

Publish stubs and sync them to AI agents:

```shell
uv run python artisan ai:skills --sync
```
