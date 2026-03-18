# MCP Resource Server

A Model Context Protocol (MCP) server that exposes read-only system resources.

## Features

Exposes the following resources:

| URI | Description |
|-----|-------------|
| `system://info` | System platform, memory, CPU, disk info |
| `system://processes` | Top 10 processes by CPU usage |
| `system://network` | Network I/O statistics |
| `system://uptime` | System uptime since boot |
| `time://current` | Current server timestamp |
| `config://app` | Sample application configuration |

## Installation

```bash
cd mcp-resource-server
pip install -r requirements.txt
```

## Testing

Test the server directly:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"resources/list"}' | python3 server.py
```

Or test with MCP Inspector:
```bash
npx @anthropics/mcp-inspector python3 server.py
```

## Register with Claude

Add to your `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "resource-server": {
      "command": "python3",
      "args": ["/Users/hj/Desktop/learn-claude-code/mcp-resource-server/server.py"]
    }
  }
}
```

After adding, restart Claude to load the server.

## Usage

Once registered, you can ask Claude to read resources:
- "Show me system info"
- "What processes are running?"
- "What's the current time?"
- "Show me the network stats"
