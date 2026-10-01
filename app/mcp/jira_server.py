from mcp.server.mcpserver import MCPServer

from app.integrations.jira import create_issue, get_issue, update_issue
from app.config import JIRA_BASE_URL

mcp = MCPServer("Jira MCP Server")


@mcp.tool()
def create_jira_issue(
    project_key: str,
    summary: str,
    description: str,
    priority: str = "Medium",
) -> dict:
    """
    Create a Jira Task in the specified Jira project.
    """

    result = create_issue(
        project_key=project_key,
        summary=summary,
        description=description,
        priority=priority,
    )

    return {
        "status": "success",
        "operation": "create_jira_issue",
        "project_key": project_key,
        "issue_key": result["key"],
        "issue_id": result["id"],
        "issue_url": f"{JIRA_BASE_URL.rstrip('/')}/browse/{result['key']}",
    }


@mcp.tool()
def get_jira_issue(
    issue_key: str,
) -> dict:
    """
    Retrieve a Jira issue by its issue key.
    """

    result = get_issue(issue_key)

    fields = result["fields"]

    return {
        "status": "success",
        "operation": "get_jira_issue",
        "issue_key": result["key"],
        "project_key": result["fields"]["project"]["key"],
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "priority": (
            fields.get("priority", {}).get("name")
            if fields.get("priority")
            else None
        ),
        "issue_type": (
            fields.get("issuetype", {}).get("name")
            if fields.get("issuetype")
            else None
        ),
        "status": (
            fields.get("status", {}).get("name")
            if fields.get("status")
            else None
        ),
    }


@mcp.tool()
def update_jira_issue(
    issue_key: str,
    summary: str | None = None,
    description: str | None = None,
    priority: str | None = None,
) -> dict:
    """Update a Jira issue's summary, description, or priority."""
    result = update_issue(issue_key, summary, description, priority)
    return {
        "status": "success",
        "operation": "update_jira_issue",
        "issue_key": result["key"],
        "updated_fields": result["updated_fields"],
        "issue_url": f"{JIRA_BASE_URL.rstrip('/')}/browse/{result['key']}",
    }


if __name__ == "__main__":
    mcp.run()
