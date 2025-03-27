# unraid-api: Python Library for Unraid GraphQL API

[![PyPI version](https://badge.fury.io/py/unraid-api.svg)](https://badge.fury.io/py/unraid-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/domalab/unraid-api/actions/workflows/test.yml/badge.svg)](https://github.com/domalab/unraid-api/actions/workflows/test.yml)

A comprehensive Python library that provides a clean, intuitive interface to Unraid's GraphQL API. It enables developers to programmatically control and monitor Unraid servers with both synchronous and asynchronous support, strong typing, and intelligent error handling.

## Features

- Complete coverage of Unraid GraphQL API endpoints
- Both synchronous and asynchronous client interfaces
- Strongly-typed Pydantic models
- Comprehensive error handling
- Authentication management with token refresh
- Support for API key authentication
- Built-in query caching
- Real-time subscription support
- Extensive documentation and examples
- Command-line interface tool

## Installation

```bash
pip install unraid-api
```

**Note:** While the package is installed with `pip install unraid-api`, you import it in your code using `import unraid-api` or `from unraid-api import UnraidClient`.

## Quick Start

### Synchronous Usage

```python
from unraid_api import UnraidClient

# Connect to Unraid server with API key
client = UnraidClient("192.168.1.10", api_key="your-api-key")

# Or with username/password
client = UnraidClient("192.168.1.10")
client.login("username", "password")

# Get system info
system_info = client.get_system_info()
print(f"System version: {system_info.version}")

# Start the array
client.array.start_array()

# Get Docker containers
containers = client.docker.get_containers()
for container in containers:
    print(f"Container: {container.name}, Status: {container.status}")
```

### Asynchronous Usage

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10")
    await client.login("username", "password")
    
    # Get all Docker containers
    containers = await client.docker.get_containers()
    for container in containers:
        print(f"Container: {container.name}, Status: {container.status}")
    
    # Perform a parity check
    await client.array.start_parity_check()

asyncio.run(main())
```

### Command-line Interface

The package also includes a command-line interface for quick interactions with Unraid servers:

```bash
# Display system information
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY system

# List Docker containers
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY docker

# Show array status
unraid-cli --ip 192.168.1.10 --api-key YOUR_API_KEY array
```

## API Documentation

### Core Resources

- **Array**: Control and monitor the Unraid array
  - `start_array()`, `stop_array()`, `get_array_status()`
- **Disk**: Manage disks and storage
  - `get_disks()`, `mount_disk()`, `unmount_disk()`
- **Docker**: Control Docker containers
  - `get_containers()`, `start_container()`, `stop_container()`, `restart_container()`
- **VM**: Manage virtual machines
  - `get_vms()`, `start_vm()`, `stop_vm()`, `restart_vm()`
- **System**: System operations and information
  - `reboot()`, `shutdown()`, `get_system_info()`
- **User**: Manage users and permissions
  - `get_users()`, `add_user()`, `delete_user()`
- **Notification**: Handle Unraid notifications
  - `get_notifications()`, `create_notification()`, `archive_notification()`

## Advanced Usage

### Real-time Subscriptions

```python
import asyncio
from unraid_api import AsyncUnraidClient

async def main():
    client = AsyncUnraidClient("192.168.1.10")
    await client.login("username", "password")
    
    # Subscribe to Docker container updates
    async for update in client.docker.subscribe_to_containers():
        print(f"Container update: {update.name} is now {update.status}")

asyncio.run(main())
```

### Error Handling

```python
from unraid_api import UnraidClient
from unraid_api.exceptions import AuthenticationError, ConnectionError, GraphQLError

try:
    client = UnraidClient("192.168.1.10")
    client.login("username", "wrong-password")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
except GraphQLError as e:
    print(f"GraphQL error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
