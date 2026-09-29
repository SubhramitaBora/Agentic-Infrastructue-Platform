import asyncio

from app.mcp.gateway import mcp_gateway


async def main():

    print("Calling Jira MCP Server through MCP Gateway...")

    result = await mcp_gateway.call_jira(
        tool_name="get_jira_issue",
        arguments={
            "issue_key": "AW-13"
        },
    )

    print("\nResult:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())