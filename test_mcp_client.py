import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    project_root = Path(__file__).resolve().parent

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            str(project_root / "app" / "mcp" / "jira_server.py")
        ],
        env={
            **os.environ,
            "PYTHONPATH": str(project_root),
        },
    )

    print("Starting Jira MCP Server...")

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            print("Initializing MCP connection...")

            await session.initialize()

            print("MCP connection established.")

            result = await session.list_tools()

            print("\nAvailable Jira MCP tools:\n")

            for tool in result.tools:
                print(f"- {tool.name}")

            print("\nMCP connection successful.")


if __name__ == "__main__":
    asyncio.run(main())