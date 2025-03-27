import os
import sys
from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from mcp.server.models import InitializationOptions

# Only load from .env file if we're not running tests
# This allows tests to set their own environment variables
if not os.environ.get('CODELOGIC_TEST_MODE'):
    load_dotenv()
    print(f"CODELOGIC_SERVER_HOST: {os.environ.get('CODELOGIC_SERVER_HOST')}", file=sys.stderr)
server = Server("codelogic-mcp-server")

# Import handlers
from .handlers import handle_list_tools, handle_call_tool

async def main():
    try:
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="codelogic-mcp-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                    instructions="When asked to modify an existing code method, invoke the get-impact mcp tool against the code provided and any methods that you are proposing changes to.  Make sure the results sent back from the tool are highlighted as impacts for the given method.",
                ),
            )
    except Exception as e:
        import traceback
        print(f"Error in MCP server: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
