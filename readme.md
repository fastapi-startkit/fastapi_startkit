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
**without calling a real model provider**. Both helpers return a chat model you
hand to `create_agent(model=...)`.

### `Agent.fake()` — pattern-based stubbing

Map prompt patterns to canned responses. A match never touches the network. Keys
are glob/substring patterns matched against the latest user message; a
`tool:<name>` key matches the turn that follows that tool's execution.

```python
from agent_testing import Agent
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.messages.tool import ToolCall

model = Agent.fake({
    "*python*": AIMessage(content="", tool_calls=[
        ToolCall(name="search_jobs", args={"query": "python"}, id="call_1"),
    ]),
    "tool:search_jobs": AIMessage(content="I found a Python Developer role at Shopify."),
})

agent = create_agent(model=model, tools=[search_jobs])
agent.invoke({"messages": [{"role": "user", "content": "find me a python job"}]})

assert model.call_count == 2
```

Pass a list instead of a mapping to return responses in sequence, or a single
`AIMessage`/`str` to answer every call with the same response.

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
