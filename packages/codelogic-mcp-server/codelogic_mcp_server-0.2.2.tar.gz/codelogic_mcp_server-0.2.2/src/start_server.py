import os
import sys
import io
import locale
import asyncio

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codelogic_mcp_server.server import main
import debugpy

if __name__ == "__main__":
    print("Starting MCP Server...", file=sys.stderr)
    
    # Set up debugging
    try:
        debugpy.listen(("127.0.0.1", 5679))
        print("Debugpy listening on port 5679", file=sys.stderr)
    except Exception as e:
        print(f"Debug setup failed: {e}", file=sys.stderr)
        
    # Run the server
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        print(f"Error in MCP server: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)