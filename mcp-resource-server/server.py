#!/usr/bin/env python3
"""MCP Resource Server - Exposes read-only data resources"""

import json
import platform
import psutil
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextResourceContents


# Create server instance
server = Server("resource-server")


# Store resources in memory
RESOURCES = {}


def refresh_resources():
    """Refresh the resource registry with current system data"""
    global RESOURCES
    
    # System info resource
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
    }
    
    # Memory info
    memory = psutil.virtual_memory()
    system_info["memory"] = {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "percent": memory.percent,
    }
    
    # CPU info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    system_info["cpu"] = {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": cpu_count,
        "current_percent": cpu_percent,
    }
    
    # Disk info
    disk = psutil.disk_usage('/')
    system_info["disk"] = {
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "percent": disk.percent,
    }
    
    RESOURCES["system://info"] = {
        "uri": "system://info",
        "name": "System Information",
        "description": "Current system platform, memory, CPU, and disk info",
        "mime_type": "application/json",
        "content": json.dumps(system_info, indent=2),
    }
    
    # Process list resource
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": round(proc.info['memory_percent'], 2),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage and take top 10
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        top_processes = processes[:10]
        
        RESOURCES["system://processes"] = {
            "uri": "system://processes",
            "name": "Top Processes",
            "description": "Top 10 processes by CPU usage",
            "mime_type": "application/json",
            "content": json.dumps(top_processes, indent=2),
        }
    except Exception:
        pass
    
    # Network info
    net_io = psutil.net_io_counters()
    network_info = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
    }
    
    RESOURCES["system://network"] = {
        "uri": "system://network",
        "name": "Network Statistics",
        "description": "Network I/O counters",
        "mime_type": "application/json",
        "content": json.dumps(network_info, indent=2),
    }
    
    # Server uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    RESOURCES["system://uptime"] = {
        "uri": "system://uptime",
        "name": "System Uptime",
        "description": "How long since system boot",
        "mime_type": "text/plain",
        "content": f"Uptime: {uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m",
    }
    
    # Current timestamp
    RESOURCES["time://now"] = {
        "uri": "time://now",
        "name": "Current Time",
        "description": "Current server timestamp",
        "mime_type": "text/plain",
        "content": datetime.now().isoformat(),
    }
    
    # Sample config resource (simulated)
    sample_config = {
        "app_name": "MCP Resource Server",
        "version": "1.0.0",
        "features": ["system_info", "processes", "network", "time"],
        "settings": {
            "refresh_interval": 60,
            "max_processes_shown": 10,
            "log_level": "info",
        }
    }
    RESOURCES["config://app"] = {
        "uri": "config://app",
        "name": "Application Config",
        "description": "Sample application configuration",
        "mime_type": "application/json",
        "content": json.dumps(sample_config, indent=2),
    }


# Initial load
refresh_resources()


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources"""
    return [
        Resource(
            uri=res["uri"],
            name=res["name"],
            description=res["description"],
            mimeType=res.get("mime_type", "text/plain"),
        )
        for res in RESOURCES.values()
    ]


@server.read_resource()
async def read_resource(uri: str) -> TextResourceContents:
    """Read a specific resource by URI"""
    # Refresh system resources before reading
    refresh_resources()
    
    if uri not in RESOURCES:
        raise ValueError(f"Resource not found: {uri}")
    
    res = RESOURCES[uri]
    return TextResourceContents(
        uri=uri,
        mimeType=res.get("mime_type", "text/plain"),
        text=res["content"],
    )


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read, write):
        await server.run(
            read,
            write,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
