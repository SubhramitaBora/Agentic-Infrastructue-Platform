from app.llm.hydra_client import ask_hydra
from app.agents.jira_agent import jira_agent
from app.agents.github_agent import github_agent


async def devops_agent(request: str) -> dict:

    prompt = f"""
You are the DevOps Agent for an Infrastructure Operations Platform.

Analyze the user's request and decide which specialist agent should handle it.

Available agents:

1. jira
   - Jira issues
   - Jira tasks
   - Jira projects
   - Jira tickets

2. github
   - GitHub repositories
   - GitHub issues
   - GitHub pull requests
   - GitHub operations

3. unknown
   - Request does not clearly belong to Jira or GitHub

User request:
{request}

Respond with ONLY one word:
jira
github
unknown
"""

    decision = await ask_hydra(prompt)

    decision = decision.strip().lower()

    if "jira" in decision:
        return await jira_agent(request)

    if "github" in decision:
        return await github_agent(request)

    return {
        "agent": "devops_agent",
        "status": "failed",
        "request": request,
        "message": "Hydra could not determine the appropriate specialist agent.",
        "hydra_decision": decision,
    }