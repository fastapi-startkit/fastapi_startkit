from langchain.agents import create_agent
from langchain_core.tools import tool


@tool
def search_jobs(query: str) -> list[dict]:
    """Search the job board for roles matching the query."""
    jobs = [
        {"title": "Python Developer", "company": "Shopify", "location": "Remote"},
        {"title": "Data Engineer", "company": "Google", "location": "Remote"},
    ]
    return [job for job in jobs if query.lower() in job["title"].lower()] or jobs


class JobAssistant:
    async def reply(self, message: str) -> str:
        agent = create_agent(
            model="google_genai:gemini-2.5-flash",
            system_prompt="You help users find jobs.",
            tools=[search_jobs],
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
        return result["messages"][-1].content
