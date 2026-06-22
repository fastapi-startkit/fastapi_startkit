import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.messages.tool import ToolCall

from agent_testing import Agent
from agent_testing import binding
from tests.agents.support import search_jobs

# These agents are built exactly like production code: a provider:name string and
# no credentials. They only run because Agent.fake() swapped the resolver globally.
STRING_MODEL = "google_genai:gemini-2.5-flash"


def build_agent():
    return create_agent(model=STRING_MODEL, system_prompt="You are helpful", tools=[search_jobs])


def run(prompt):
    return build_agent().invoke({"messages": [{"role": "user", "content": prompt}]})


class TestGlobalSwap:
    def test_intercepts_string_model_without_injection(self):
        Agent.fake({"*jobs*": AIMessage(content="Here are 3 Python jobs.")})

        result = run("suggest me jobs")

        assert result["messages"][-1].content == "Here are 3 Python jobs."

    def test_default_fake_returns_empty_response(self):
        Agent.fake()

        assert run("anything at all")["messages"][-1].content == ""

    def test_full_tool_loop_through_global_fake(self):
        Agent.fake(
            {
                "*python*": AIMessage(
                    content="",
                    tool_calls=[ToolCall(name="search_jobs", args={"query": "python"}, id="call_1")],
                ),
                "tool:search_jobs": AIMessage(content="Found a Python Developer role at Shopify."),
            }
        )

        assert run("find a python job")["messages"][-1].content == "Found a Python Developer role at Shopify."

    def test_context_manager_resets_on_exit(self):
        with Agent.fake({"*hi*": "hello"}):
            assert binding.is_faking()
        assert not binding.is_faking()

    def test_reset_restores_resolver(self):
        Agent.fake()
        assert binding.is_faking()
        Agent.reset()
        assert not binding.is_faking()


class TestGlobalAssertions:
    def test_assert_invoked_with_and_without_pattern(self):
        Agent.fake({"*jobs*": AIMessage(content="ok")})
        run("suggest me jobs")

        Agent.assert_invoked()
        Agent.assert_invoked("*jobs*")
        Agent.assert_invoked_count(1)

    def test_assert_invoked_pattern_mismatch_fails(self):
        Agent.fake({"*jobs*": AIMessage(content="ok")})
        run("suggest me jobs")

        with pytest.raises(AssertionError):
            Agent.assert_invoked("*weather*")

    def test_assert_nothing_invoked(self):
        Agent.fake({"*jobs*": AIMessage(content="ok")})

        Agent.assert_nothing_invoked()

        with pytest.raises(AssertionError):
            Agent.assert_invoked()
