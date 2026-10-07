import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class MCPGateway:

    async def call_jira(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ):

        server_params = StdioServerParameters(
            command=sys.executable,
            args=[
                str(PROJECT_ROOT / "app" / "mcp" / "jira_server.py")
            ],
            env={
                **os.environ,
                "PYTHONPATH": str(PROJECT_ROOT),
            },
        )

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    async def call_github(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ):

        server_params = StdioServerParameters(
            command=sys.executable,
            args=[
                str(PROJECT_ROOT / "app" / "mcp" / "github_server.py")
            ],
            env={
                **os.environ,
                "PYTHONPATH": str(PROJECT_ROOT),
            },
        )

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    async def call_confluence(self, tool_name: str, arguments: dict[str, Any]):
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(PROJECT_ROOT / "app" / "mcp" / "confluence_server.py")],
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await session.call_tool(tool_name, arguments)


mcp_gateway = MCPGateway()
