#!/usr/bin/env python
"""
Simple runner script for the Kagi Bridge MCP server.
"""
import sys
from kagi_bridge_mcp.server import main

if __name__ == "__main__":
    sys.exit(main())
