import json

import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.messages.tool import ToolCall

from agent_testing import Agent, CassetteMiss
from tests.agents.support import search_jobs


def cassette_path(tmp_path):
    return str(tmp_path / "cassettes" / "chat.json")


class TestRecordReplay:
    def test_records_then_replays_without_calling_model_again(self, tmp_path):
        path = cassette_path(tmp_path)
        real = Agent.fake({"hi": "recorded answer"})

        recorder = Agent.record(real, cassette=path)
        assert recorder.invoke("say hi please").content == "recorded answer"
        assert real.call_count == 1

        # A fresh recorder loading the same cassette must replay from disk and
        # never touch the underlying model (the sentinel raises if invoked).
        sentinel = Agent.fake()
        replayer = Agent.record(sentinel, cassette=path)
        assert replayer.invoke("say hi please").content == "recorded answer"
        assert sentinel.call_count == 0

    def test_cassette_file_format(self, tmp_path):
        path = cassette_path(tmp_path)
        Agent.record(Agent.fake({"hi": "answer"}), cassette=path).invoke("hi")

        document = json.loads(open(path).read())
        assert document["version"] == 1
        assert len(document["interactions"]) == 1
        interaction = document["interactions"][0]
        assert set(interaction) == {"key", "request", "response"}

    def test_replay_mode_misses_raise(self, tmp_path):
        replayer = Agent.record(Agent.fake(), cassette=cassette_path(tmp_path), mode="replay")

        with pytest.raises(CassetteMiss):
            replayer.invoke("nothing recorded")

    def test_record_mode_overwrites_existing(self, tmp_path):
        path = cassette_path(tmp_path)
        Agent.record(Agent.fake({"hi": "first"}), cassette=path).invoke("hi")

        recorder = Agent.record(Agent.fake({"hi": "second"}), cassette=path, mode="record")
        assert recorder.invoke("hi").content == "second"

    def test_invalid_mode_raises(self, tmp_path):
        with pytest.raises(ValueError):
            Agent.record(Agent.fake(), cassette=cassette_path(tmp_path), mode="bogus")

    async def test_async_record_then_replay(self, tmp_path):
        path = cassette_path(tmp_path)
        real = Agent.fake({"hi": "async answer"})

        recorder = Agent.record(real, cassette=path)
        assert (await recorder.ainvoke("hi")).content == "async answer"

        sentinel = Agent.fake()
        replayer = Agent.record(sentinel, cassette=path)
        assert (await replayer.ainvoke("hi")).content == "async answer"
        assert sentinel.call_count == 0


class TestRecordThroughAgent:
    def test_full_tool_loop_records_and_replays(self, tmp_path):
        path = cassette_path(tmp_path)
        real = Agent.fake(
            [
                AIMessage(
                    content="",
                    tool_calls=[ToolCall(name="search_jobs", args={"query": "python"}, id="call_1")],
                ),
                AIMessage(content="Found a Python Developer role."),
            ]
        )

        recorder = Agent.record(real, cassette=path)
        agent = create_agent(model=recorder, tools=[search_jobs])
        first = agent.invoke({"messages": [{"role": "user", "content": "find a python job"}]})
        assert first["messages"][-1].content == "Found a Python Developer role."

        sentinel = Agent.fake()
        replay_agent = create_agent(model=Agent.record(sentinel, cassette=path), tools=[search_jobs])
        second = replay_agent.invoke({"messages": [{"role": "user", "content": "find a python job"}]})
        assert second["messages"][-1].content == "Found a Python Developer role."
        assert sentinel.call_count == 0
