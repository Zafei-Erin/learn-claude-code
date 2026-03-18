#!/usr/bin/env python3
"""Test script for MCP Resource Server"""

import json
import subprocess
import sys

def test_server():
    """Test the MCP resource server"""
    
    # Start the server process
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/Users/hj/Desktop/learn-claude-code/mcp-resource-server"
    )
    
    try:
        # Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialize
        stdout, stderr = proc.communicate(
            input=json.dumps(init_request) + "\n",
            timeout=5
        )
        print("Initialize response:")
        print(stdout)
        if stderr:
            print("Stderr:", stderr)
        
        # Send initialized notification (no response expected)
        initialized = {"jsonrpc": "2.0", "method": "initialized", "params": {}}
        proc.stdin.write(json.dumps(initialized) + "\n")
        proc.stdin.flush()
        
        # List resources
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "resources/list"
        }
        
        stdout, stderr = proc.communicate(
            input=json.dumps(list_request) + "\n",
            timeout=5
        )
        print("\nList resources response:")
        print(stdout)
        
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    test_server()
