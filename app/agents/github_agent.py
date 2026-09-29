import json
import re

from app.mcp.gateway import mcp_gateway


def extract_repository(request: str):
    """
    Extract a GitHub repository in the form:
    owner/repository

    Supports:
    - SubhramitaBora/Agentic-Workflow
    - https://github.com/SubhramitaBora/Agentic-Workflow
    """

    # Check for a GitHub URL
    url_match = re.search(
        r"github\.com/([^/\s]+)/([^/\s#?]+)",
        request,
        re.IGNORECASE,
    )

    if url_match:
        owner = url_match.group(1)
        repo = url_match.group(2).removesuffix(".git")

        return owner, repo

    # Check for owner/repository format
    repo_match = re.search(
        r"\b([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)\b",
        request,
    )

    if repo_match:
        owner = repo_match.group(1)
        repo = repo_match.group(2)

        return owner, repo

    return None, None


async def github_agent(request: str) -> dict:
    """
    GitHub specialist agent.

    Determines the GitHub operation and repository,
    then routes the request through the MCP Gateway.
    """

    request_lower = request.lower()

    # --------------------------------
    # Extract repository
    # --------------------------------

    owner, repo = extract_repository(request)

    if not owner or not repo:
        return {
            "agent": "github_agent",
            "status": "failed",
            "request": request,
            "message": (
                "Could not determine the GitHub repository. "
                "Please specify it as owner/repository, "
                "for example: SubhramitaBora/Agentic-Workflow."
            ),
        }

    # --------------------------------
    # Get Pull Request
    # --------------------------------

    if "pull request" in request_lower or "pull-request" in request_lower:

        words = request.split()
        pull_number = None

        for word in words:
            cleaned = word.strip(".,!?()[]#")

            if cleaned.isdigit():
                pull_number = int(cleaned)
                break

        if pull_number is None:
            return {
                "agent": "github_agent",
                "status": "failed",
                "request": request,
                "message": (
                    "Could not find a pull request number "
                    "such as 6."
                ),
            }

        result = await mcp_gateway.call_github(
            tool_name="get_github_pull_request",
            arguments={
                "owner": owner,
                "repo": repo,
                "pull_number": pull_number,
            },
        )

        data = json.loads(result.content[0].text)

        return {
            "agent": "github_agent",
            "status": "completed",
            "operation": "get_github_pull_request",
            "repository": f"{owner}/{repo}",
            "request": request,
            "mcp_result": data,
        }

    # --------------------------------
    # Get Repository
    # --------------------------------

    if "repository" in request_lower or "repo" in request_lower:

        result = await mcp_gateway.call_github(
            tool_name="get_github_repository",
            arguments={
                "owner": owner,
                "repo": repo,
            },
        )

        data = json.loads(result.content[0].text)

        return {
            "agent": "github_agent",
            "status": "completed",
            "operation": "get_github_repository",
            "repository": f"{owner}/{repo}",
            "request": request,
            "mcp_result": data,
        }

    # --------------------------------
    # Get GitHub Issue
    # --------------------------------

    if "get" in request_lower and "issue" in request_lower:

        words = request.split()
        issue_number = None

        for word in words:
            cleaned = word.strip(".,!?()[]#")

            if cleaned.isdigit():
                issue_number = int(cleaned)
                break

        if issue_number is None:
            return {
                "agent": "github_agent",
                "status": "failed",
                "request": request,
                "message": (
                    "Could not find a GitHub issue number "
                    "such as 12."
                ),
            }

        result = await mcp_gateway.call_github(
            tool_name="get_github_issue",
            arguments={
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
            },
        )

        data = json.loads(result.content[0].text)

        return {
            "agent": "github_agent",
            "status": "completed",
            "operation": "get_github_issue",
            "repository": f"{owner}/{repo}",
            "request": request,
            "mcp_result": data,
        }

    # --------------------------------
    # Create GitHub Issue
    # --------------------------------

    result = await mcp_gateway.call_github(
        tool_name="create_github_issue",
        arguments={
            "owner": owner,
            "repo": repo,
            "title": request,
            "body": request,
        },
    )

    data = json.loads(result.content[0].text)

    return {
        "agent": "github_agent",
        "status": "completed",
        "operation": "create_github_issue",
        "repository": f"{owner}/{repo}",
        "request": request,
        "mcp_result": data,
    }