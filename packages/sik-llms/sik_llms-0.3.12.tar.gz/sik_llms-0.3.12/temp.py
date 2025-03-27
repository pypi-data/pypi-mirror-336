import asyncio
from sik_llms.mcp_manager import MCPClientManager


mcp_servers = {
    "mcpServers": {
        "fake-server-text": {
            "command": "uv",
            "args": [
                "run",
                "--directory",
                './tests/test_files/',
                "mcp",
                "run",
                "mcp_fake_server_text.py",
            ],
        },
    },
}


async def main():
    async with MCPClientManager(mcp_servers) as manager:
        tools = manager.get_tool_infos()
        
        result = await manager.call_tool('reverse_text', args={'text': 'hello'})
        print(result)
        # print(tools)


if __name__ == '__main__':
    asyncio.run(main())