from langchain_core.tools import tool


@tool
def search_jobs(query: str) -> list[dict]:
    """Search the job board for roles matching the query."""
    jobs = [
        {"title": "Python Developer", "company": "Shopify", "location": "Remote"},
        {"title": "Senior Backend Engineer", "company": "Amazon", "location": "Vancouver"},
        {"title": "Data Engineer", "company": "Google", "location": "Remote"},
    ]
    return [job for job in jobs if query.lower() in job["title"].lower()] or jobs
