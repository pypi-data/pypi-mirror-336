# PyUnraid: Python Library for Unraid GraphQL API

A comprehensive Python library that provides a clean, intuitive interface to Unraid's GraphQL API. It enables developers to programmatically control and monitor Unraid servers with both synchronous and asynchronous support, strong typing, and intelligent error handling.

## Installation

```bash
pip install pyunraid
```

## Usage

### Simple Synchronous Example

```python
from pyunraid import UnraidClient

# Connect to Unraid server
client = UnraidClient("192.168.1.10")
client.login("username", "password")

# Get system info
system_info = client.get_system_info()
print(f"System version: {system_info.version}")

# Start the array
client.system.start_array()
```

### Async Example

```python
import asyncio
from pyunraid.async_client import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10")
    await client.login("username", "password")
    
    # Get all Docker containers
    containers = await client.docker.get_containers()
    for container in containers:
        print(f"Container: {container.name}, Status: {container.status}")
    
    # Perform a parity check
    await client.system.start_parity_check()

asyncio.run(main())
```

## Features

- Complete access to Unraid GraphQL API endpoints
- Both synchronous and asynchronous interfaces
- Automatic token refresh and management
- Strongly-typed Python classes using Pydantic
- Comprehensive error handling
- Request/response logging for debugging

## License

MIT License
