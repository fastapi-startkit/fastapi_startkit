from langchain_core.tools import tool

from agent_testing import Agent


@tool
def search_jobs(query: str) -> list[dict]:
    """Search the job board for roles matching the query."""
    jobs = [
        {"title": "Python Developer", "company": "Shopify", "location": "Remote"},
        {"title": "Data Engineer", "company": "Google", "location": "Remote"},
    ]
    return [job for job in jobs if query.lower() in job["title"].lower()] or jobs


class JobAssistant(Agent):
    system_prompt = "You help users find jobs."

    def tools(self):
        return [search_jobs]
