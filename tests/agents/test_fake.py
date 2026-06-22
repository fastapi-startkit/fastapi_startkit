import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.messages.tool import ToolCall

from agent_testing import Agent, NoFakeResponse
from tests.agents.support import search_jobs


def build_agent(model):
    return create_agent(model=model, system_prompt="You are a helpful assistant", tools=[search_jobs])


def run(agent, prompt):
    return agent.invoke({"messages": [{"role": "user", "content": prompt}]})


class TestFakePatternMatching:
    def test_pattern_returns_mapped_response(self):
        model = Agent.fake({"*python*": AIMessage(content="A Python role at Shopify.")})

        result = run(build_agent(model), "find me a python job")

        assert result["messages"][-1].content == "A Python role at Shopify."
        assert model.call_count == 1

    def test_substring_pattern_without_globs(self):
        model = Agent.fake({"weather": "It is sunny."})

        assert run(build_agent(model), "how is the weather today")["messages"][-1].content == "It is sunny."

    def test_full_tool_loop_without_api(self):
        model = Agent.fake(
            {
                "*python*": AIMessage(
                    content="",
                    tool_calls=[ToolCall(name="search_jobs", args={"query": "python"}, id="call_1")],
                ),
                "tool:search_jobs": AIMessage(content="I found a Python Developer role at Shopify."),
            }
        )

        messages = run(build_agent(model), "find me a python job")["messages"]

        assert any(isinstance(m, ToolMessage) and m.name == "search_jobs" for m in messages)
        assert messages[-1].content == "I found a Python Developer role at Shopify."
        assert model.call_count == 2

    def test_no_match_raises(self):
        model = Agent.fake({"*python*": "hi"})

        with pytest.raises(NoFakeResponse):
            run(build_agent(model), "tell me a joke")


class TestFakeSequential:
    def test_list_returns_responses_in_order(self):
        model = Agent.fake(
            [
                AIMessage(
                    content="",
                    tool_calls=[ToolCall(name="search_jobs", args={"query": "python"}, id="call_1")],
                ),
                AIMessage(content="Here is the role I found."),
            ]
        )

        messages = run(build_agent(model), "anything")["messages"]

        assert messages[-1].content == "Here is the role I found."
        assert model.call_count == 2

    def test_exhausted_sequence_raises(self):
        model = Agent.fake(["only one response"])
        # The single response triggers a tool-less final turn, so one call suffices;
        # a second direct call must raise.
        model.invoke("first")
        with pytest.raises(NoFakeResponse):
            model.invoke("second")


class TestFakeDirectInvoke:
    def test_invoke_returns_ai_message(self):
        model = Agent.fake({"hi": AIMessage(content="hello there")})

        assert model.invoke("hi").content == "hello there"

    async def test_async_invoke(self):
        model = Agent.fake({"hi": "hello there"})

        result = await model.ainvoke("say hi")

        assert result.content == "hello there"
        assert model.call_count == 1

    def test_constant_response_for_any_input(self):
        model = Agent.fake(AIMessage(content="always this"))

        assert model.invoke("anything").content == "always this"
        assert model.invoke("something else").content == "always this"
