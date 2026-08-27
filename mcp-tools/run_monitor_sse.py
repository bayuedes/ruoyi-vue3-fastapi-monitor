"""以 SSE 模式启动 monitor_server (Langflow 可通过 http://127.0.0.1:8092/sse 接入)"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from monitor_server import mcp  # noqa: E402

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8092"))
    print(f"Starting monitor MCP server in SSE mode on {host}:{port}/sse ...", flush=True)
    mcp.run(transport="sse", host=host, port=port)
