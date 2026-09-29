from app.agents.jira_agent import jira_agent
from app.agents.github_agent import github_agent


async def devops_agent(request: str) -> dict:
    """
    Central DevOps agent responsible for routing
    the request to the appropriate specialist agent.
    """

    request_lower = request.lower()

    if "jira" in request_lower:
        return await jira_agent(request)

    if "github" in request_lower:
        return await github_agent(request)

    return {
        "agent": "unknown",
        "status": "failed",
        "request": request,
        "message": (
            "I could not determine whether this is "
            "a Jira or GitHub request."
        ),
    }