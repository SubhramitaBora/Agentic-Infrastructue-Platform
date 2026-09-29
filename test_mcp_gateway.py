import asyncio

from app.mcp.gateway import mcp_gateway


async def main():

    print("=== Jira MCP Test ===")

    jira_result = await mcp_gateway.call_jira(
        tool_name="get_jira_issue",
        arguments={
            "issue_key": "AW-13"
        },
    )

    print("\nJira Result:")
    print(jira_result)

    print("\n" + "=" * 50)

    print("\n=== GitHub MCP Test ===")

    github_result = await mcp_gateway.call_github(
        tool_name="get_github_repository",
        arguments={},
    )

    print("\nGitHub Result:")
    print(github_result)


if __name__ == "__main__":
    asyncio.run(main())