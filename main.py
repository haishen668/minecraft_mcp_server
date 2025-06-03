# main.py

import asyncio
from mcp.server.stdio import stdio_server
from mcp.server import Server
from resources import register_all_resources
from tools import register_all_tools

app = Server("我的世界mcp")

# 注册资源和工具
register_all_resources(app)
register_all_tools(app)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

def run_main():
    """作为PyPI包的入口点"""
    asyncio.run(main())

if __name__ == "__main__":
    run_main()