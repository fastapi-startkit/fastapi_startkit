import pytest

from agent_testing import Agent


@pytest.fixture(autouse=True)
def _reset_agent_fake():
    """Tear down any global fake after each test so state never leaks across tests."""
    yield
    Agent.reset()
