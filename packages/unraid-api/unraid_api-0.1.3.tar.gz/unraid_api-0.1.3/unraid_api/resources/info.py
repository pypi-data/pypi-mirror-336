"""System information resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class InfoResource:
    """System information resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the info resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information.
        
        Returns:
            System information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetSystemInfo {
            info {
                os {
                    platform
                    distro
                    release
                    kernel
                    uptime
                }
                cpu {
                    manufacturer
                    brand
                    cores
                    threads
                }
                memory {
                    total
                    free
                    used
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "info" not in result:
            raise APIError("Invalid response format: missing info field")
        
        return result["info"]
    
    def reboot(self) -> Dict[str, Any]:
        """Reboot the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation Reboot {
            reboot {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("reboot", {}).get("success", False):
            message = result.get("reboot", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to reboot: {message}")
        
        return result["reboot"]
    
    def shutdown(self) -> Dict[str, Any]:
        """Shutdown the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation Shutdown {
            shutdown {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("shutdown", {}).get("success", False):
            message = result.get("shutdown", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to shutdown: {message}")
        
        return result["shutdown"]
    
    def get_docker_info(self) -> Dict[str, Any]:
        """Get Docker information.
        
        Returns:
            Docker information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDockerInfo {
            dockerInfo {
                enabled
                version
                status
                rootPath
                configPath
                imagePath
                autostart
                networkDefault
                customNetworks
                privileged
                logRotation
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "dockerInfo" not in result:
            raise APIError("Invalid response format: missing dockerInfo field")
        
        return result["dockerInfo"]
    
    def get_vm_info(self) -> Dict[str, Any]:
        """Get VM information.
        
        Returns:
            VM information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMInfo {
            vmInfo {
                enabled
                version
                status
                corePath
                configPath
                imagePath
                autostart
                winVmCount
                linuxVmCount
                otherVmCount
                CPUisolatedCores
                PCIeiommuGroups
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "vmInfo" not in result:
            raise APIError("Invalid response format: missing vmInfo field")
        
        return result["vmInfo"]


class AsyncInfoResource:
    """Async system information resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the info resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information.
        
        Returns:
            System information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetSystemInfo {
            info {
                os {
                    platform
                    distro
                    release
                    kernel
                    uptime
                }
                cpu {
                    manufacturer
                    brand
                    cores
                    threads
                }
                memory {
                    total
                    free
                    used
                }
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "info" not in result:
            raise APIError("Invalid response format: missing info field")
        
        return result["info"]
    
    async def reboot(self) -> Dict[str, Any]:
        """Reboot the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation Reboot {
            reboot {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("reboot", {}).get("success", False):
            message = result.get("reboot", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to reboot: {message}")
        
        return result["reboot"]
    
    async def shutdown(self) -> Dict[str, Any]:
        """Shutdown the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation Shutdown {
            shutdown {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("shutdown", {}).get("success", False):
            message = result.get("shutdown", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to shutdown: {message}")
        
        return result["shutdown"]
    
    async def get_docker_info(self) -> Dict[str, Any]:
        """Get Docker information.
        
        Returns:
            Docker information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDockerInfo {
            dockerInfo {
                enabled
                version
                status
                rootPath
                configPath
                imagePath
                autostart
                networkDefault
                customNetworks
                privileged
                logRotation
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "dockerInfo" not in result:
            raise APIError("Invalid response format: missing dockerInfo field")
        
        return result["dockerInfo"]
    
    async def get_vm_info(self) -> Dict[str, Any]:
        """Get VM information.
        
        Returns:
            VM information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMInfo {
            vmInfo {
                enabled
                version
                status
                corePath
                configPath
                imagePath
                autostart
                winVmCount
                linuxVmCount
                otherVmCount
                CPUisolatedCores
                PCIeiommuGroups
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "vmInfo" not in result:
            raise APIError("Invalid response format: missing vmInfo field")
        
        return result["vmInfo"]
