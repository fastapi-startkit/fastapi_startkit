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

The `agent_testing` package is a lightweight harness for testing LangChain agents
**without calling a real model provider**, in the spirit of Laravel's `Http::fake()`.

### `Agent.fake()` — global stubbing

Call `Agent.fake()` once and **every** agent built afterward via
`create_agent(model="provider:name")` returns the stub — no injection, no changes
to your agent code. This lets you hit your real backend endpoint and assert on the
response while the model never touches the network:

```python
from agent_testing import Agent
from langchain_core.messages import AIMessage

class TestChatApi(TestCase):  # your HttpTestCase
    async def test_suggest_jobs(self):
        with Agent.fake({"*jobs*": AIMessage(content="Here are 3 Python jobs.")}):
            response = await self.post("/chat", json={"message": "suggest me jobs"})

        assert response.status_code == 200
        assert "Python jobs" in response.json()["reply"]
        Agent.assert_invoked("*jobs*")
```

Keys are glob/substring patterns matched against the latest user message; a
`tool:<name>` key matches the model turn that follows that tool's execution. Pass a
list to return responses in sequence, a single `AIMessage`/`str` for a constant
reply, or nothing (`Agent.fake()`) to answer every call with an empty response.

Use it as a context manager (resets on exit) or call `Agent.reset()` in teardown —
an autouse fixture is the cleanest way to keep tests isolated:

```python
@pytest.fixture(autouse=True)
def _reset_agents():
    yield
    Agent.reset()
```

Assertions mirror the facade style: `Agent.assert_invoked(pattern=None)`,
`Agent.assert_invoked_count(n)`, and `Agent.assert_nothing_invoked()`.

The returned model also works as a direct injection if you prefer to pass it
explicitly: `create_agent(model=Agent.fake({...}), tools=[...])`.

### `Agent.record()` — record then replay

Wrap a real model. The first run records each response to a cassette file; later
runs replay from disk with no network I/O. Use `mode="replay"` in CI to fail on
any un-recorded request, or `mode="record"` to refresh the cassette.

```python
model = Agent.record(real_model, cassette="tests/cassettes/chat.json")
agent = create_agent(model=model, tools=[search_jobs])
agent.invoke({"messages": [{"role": "user", "content": "find me a python job"}]})
```

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
