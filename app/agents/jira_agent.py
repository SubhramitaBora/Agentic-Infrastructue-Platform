import json
import re

from app.mcp.gateway import mcp_gateway


def extract_issue_key(request: str):
    """
    Extract a Jira issue key such as:
    AD-4
    DEV-123
    PROJECT-42
    """

    match = re.search(
        r"\b([A-Za-z][A-Za-z0-9_]*-\d+)\b",
        request,
    )

    if match:
        return match.group(1).upper()

    return None


def extract_project_key(request: str):
    """
    Extract a Jira project key when creating an issue.

    Example:
    'Create a Jira issue in DEV for API latency'
    -> DEV
    """

    match = re.search(
        r"\b(?:in|project)\s+([A-Za-z][A-Za-z0-9_]*)\b",
        request,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).upper()

    return None


async def jira_agent(request: str) -> dict:
    """
    Jira specialist agent.

    Determines the Jira operation and project,
    then routes the request through the MCP Gateway.
    """

    request_lower = request.lower()

    # --------------------------------
    # Get Jira Issue
    # --------------------------------

    if "get" in request_lower and "issue" in request_lower:

        issue_key = extract_issue_key(request)

        if not issue_key:
            return {
                "agent": "jira_agent",
                "status": "failed",
                "request": request,
                "message": (
                    "Could not find a Jira issue key. "
                    "Please provide one such as AD-4 or DEV-123."
                ),
            }

        result = await mcp_gateway.call_jira(
            tool_name="get_jira_issue",
            arguments={
                "issue_key": issue_key,
            },
        )

        data = json.loads(result.content[0].text)

        return {
            "agent": "jira_agent",
            "status": "completed",
            "operation": "get_jira_issue",
            "issue_key": issue_key,
            "request": request,
            "mcp_result": data,
        }

    # --------------------------------
    # Extract Project
    # --------------------------------

    project_key = extract_project_key(request)

    if not project_key:
        return {
            "agent": "jira_agent",
            "status": "failed",
            "request": request,
            "message": (
                "Could not determine the Jira project. "
                "Please specify a project key, "
                "for example: 'Create a Jira issue in AD ...'"
            ),
        }

    # --------------------------------
    # Determine Priority
    # --------------------------------

    if "highest" in request_lower:
        priority = "Highest"
    elif "high" in request_lower:
        priority = "High"
    elif "low" in request_lower:
        priority = "Low"
    else:
        priority = "Medium"

    # --------------------------------
    # Create Jira Issue
    # --------------------------------

    result = await mcp_gateway.call_jira(
        tool_name="create_jira_issue",
        arguments={
            "project_key": project_key,
            "summary": request,
            "description": request,
            "priority": priority,
        },
    )

    data = json.loads(result.content[0].text)

    return {
        "agent": "jira_agent",
        "status": "completed",
        "operation": "create_jira_issue",
        "project_key": project_key,
        "priority": priority,
        "request": request,
        "mcp_result": data,
    }