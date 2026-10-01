from mcp.server.mcpserver import MCPServer

from app.integrations.github import (
    create_issue,
    get_issue,
    get_repository,
    get_pull_request,
    update_issue,
)

mcp = MCPServer("GitHub MCP Server")


@mcp.tool()
def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
) -> dict:
    """
    Create a GitHub issue in the specified repository.
    """

    result = create_issue(
        owner=owner,
        repo=repo,
        title=title,
        body=body,
    )

    return {
        "status": "success",
        "operation": "create_github_issue",
        "repository": f"{owner}/{repo}",
        "issue_number": result["number"],
        "issue_url": result["html_url"],
    }


@mcp.tool()
def get_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict:
    """
    Retrieve a GitHub issue from the specified repository.
    """

    result = get_issue(
        owner=owner,
        repo=repo,
        issue_number=issue_number,
    )

    return {
        "status": "success",
        "operation": "get_github_issue",
        "repository": f"{owner}/{repo}",
        "issue_number": result["number"],
        "title": result["title"],
        "body": result["body"],
        "state": result["state"],
        "url": result["html_url"],
    }


@mcp.tool()
def update_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: str | None = None,
    body: str | None = None,
    state: str | None = None,
) -> dict:
    """Update a GitHub issue's title, body, or open/closed state."""
    result = update_issue(owner, repo, issue_number, title, body, state)
    return {
        "status": "success",
        "operation": "update_github_issue",
        "repository": f"{owner}/{repo}",
        "issue_number": result["number"],
        "title": result["title"],
        "body": result["body"],
        "state": result["state"],
        "url": result["html_url"],
    }


@mcp.tool()
def get_github_repository(
    owner: str,
    repo: str,
) -> dict:
    """
    Retrieve information about a GitHub repository.
    """

    result = get_repository(
        owner=owner,
        repo=repo,
    )

    return {
        "status": "success",
        "operation": "get_github_repository",
        "repository": f"{owner}/{repo}",
        "name": result["name"],
        "full_name": result["full_name"],
        "description": result["description"],
        "default_branch": result["default_branch"],
        "private": result["private"],
        "url": result["html_url"],
    }


@mcp.tool()
def get_github_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
) -> dict:
    """
    Retrieve a GitHub pull request from the specified repository.
    """

    result = get_pull_request(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
    )

    return {
        "status": "success",
        "operation": "get_github_pull_request",
        "repository": f"{owner}/{repo}",
        "pull_number": result["number"],
        "title": result["title"],
        "body": result["body"],
        "state": result["state"],
        "merged": result["merged"],
        "url": result["html_url"],
    }


if __name__ == "__main__":
    mcp.run()
