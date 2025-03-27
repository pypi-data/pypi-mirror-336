"""Disk resource for pyunraid."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class DiskResource:
    """Disk resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the disk resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_disks(self) -> List[Dict[str, Any]]:
        """Get all disks.
        
        Returns:
            List of disks
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDisks {
            disks {
                id
                device
                name
                size
                type
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "disks" not in result:
            raise APIError("Invalid response format: missing disks field")
        
        return result["disks"]
    
    def get_disk(self, id: str) -> Dict[str, Any]:
        """Get a disk by ID.
        
        Args:
            id: The disk ID
            
        Returns:
            The disk info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDisk($id: String!) {
            disk(id: $id) {
                id
                device
                deviceId
                deviceNode
                name
                partitions {
                    number
                    name
                    fsType
                    mountpoint
                    size
                    used
                    free
                    color
                    temp
                    deviceId
                    isArray
                }
                size
                temp
                status
                interface
                model
                protocol
                rotationRate
                serial
                type
                numReads
                numWrites
                numErrors
                color
                rotational
                vendor
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(query, variables)
        
        if "disk" not in result:
            raise APIError("Invalid response format: missing disk field")
        
        return result["disk"]
    
    def mount_disk(self, id: str) -> Dict[str, Any]:
        """Mount a disk.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MountDisk($id: String!) {
            mountDisk(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("mountDisk", {}).get("success", False):
            message = result.get("mountDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mount disk: {message}")
        
        return result["mountDisk"]
    
    def unmount_disk(self, id: str) -> Dict[str, Any]:
        """Unmount a disk.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UnmountDisk($id: String!) {
            unmountDisk(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("unmountDisk", {}).get("success", False):
            message = result.get("unmountDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to unmount disk: {message}")
        
        return result["unmountDisk"]

    def format_disk(self, id: str, fs_type: str) -> Dict[str, Any]:
        """Format a disk.
        
        Args:
            id: The disk ID
            fs_type: The filesystem type
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation FormatDisk($id: String!, $fsType: String!) {
            formatDisk(id: $id, fsType: $fsType) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id,
            "fsType": fs_type
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("formatDisk", {}).get("success", False):
            message = result.get("formatDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to format disk: {message}")
        
        return result["formatDisk"]
    
    def clear_disk_statistics(self, id: str) -> Dict[str, Any]:
        """Clear disk statistics.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ClearDiskStatistics($id: String!) {
            clearDiskStatistics(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("clearDiskStatistics", {}).get("success", False):
            message = result.get("clearDiskStatistics", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to clear disk statistics: {message}")
        
        return result["clearDiskStatistics"]
    
    def mount_array_disk(self, slot: str) -> Dict[str, Any]:
        """Mount an array disk.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MountArrayDisk($slot: String!) {
            mountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("mountArrayDisk", {}).get("success", False):
            message = result.get("mountArrayDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mount array disk: {message}")
        
        return result["mountArrayDisk"]
    
    def unmount_array_disk(self, slot: str) -> Dict[str, Any]:
        """Unmount an array disk.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UnmountArrayDisk($slot: String!) {
            unmountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("unmountArrayDisk", {}).get("success", False):
            message = result.get("unmountArrayDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to unmount array disk: {message}")
        
        return result["unmountArrayDisk"]
    
    def clear_array_disk_statistics(self, slot: str) -> Dict[str, Any]:
        """Clear array disk statistics.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ClearArrayDiskStatistics($slot: String!) {
            clearArrayDiskStatistics(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("clearArrayDiskStatistics", {}).get("success", False):
            message = result.get("clearArrayDiskStatistics", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to clear array disk statistics: {message}")
        
        return result["clearArrayDiskStatistics"]


class AsyncDiskResource:
    """Async disk resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the disk resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_disks(self) -> List[Dict[str, Any]]:
        """Get all disks.
        
        Returns:
            List of disks
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDisks {
            disks {
                id
                device
                name
                size
                type
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "disks" not in result:
            raise APIError("Invalid response format: missing disks field")
        
        return result["disks"]
    
    async def get_disk(self, id: str) -> Dict[str, Any]:
        """Get a disk by ID.
        
        Args:
            id: The disk ID
            
        Returns:
            The disk info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDisk($id: String!) {
            disk(id: $id) {
                id
                device
                deviceId
                deviceNode
                name
                partitions {
                    number
                    name
                    fsType
                    mountpoint
                    size
                    used
                    free
                    color
                    temp
                    deviceId
                    isArray
                }
                size
                temp
                status
                interface
                model
                protocol
                rotationRate
                serial
                type
                numReads
                numWrites
                numErrors
                color
                rotational
                vendor
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "disk" not in result:
            raise APIError("Invalid response format: missing disk field")
        
        return result["disk"]
    
    async def mount_disk(self, id: str) -> Dict[str, Any]:
        """Mount a disk.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MountDisk($id: String!) {
            mountDisk(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("mountDisk", {}).get("success", False):
            message = result.get("mountDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mount disk: {message}")
        
        return result["mountDisk"]
    
    async def unmount_disk(self, id: str) -> Dict[str, Any]:
        """Unmount a disk.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UnmountDisk($id: String!) {
            unmountDisk(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("unmountDisk", {}).get("success", False):
            message = result.get("unmountDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to unmount disk: {message}")
        
        return result["unmountDisk"]

    async def format_disk(self, id: str, fs_type: str) -> Dict[str, Any]:
        """Format a disk.
        
        Args:
            id: The disk ID
            fs_type: The filesystem type
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation FormatDisk($id: String!, $fsType: String!) {
            formatDisk(id: $id, fsType: $fsType) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id,
            "fsType": fs_type
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("formatDisk", {}).get("success", False):
            message = result.get("formatDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to format disk: {message}")
        
        return result["formatDisk"]
    
    async def clear_disk_statistics(self, id: str) -> Dict[str, Any]:
        """Clear disk statistics.
        
        Args:
            id: The disk ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ClearDiskStatistics($id: String!) {
            clearDiskStatistics(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("clearDiskStatistics", {}).get("success", False):
            message = result.get("clearDiskStatistics", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to clear disk statistics: {message}")
        
        return result["clearDiskStatistics"]
    
    async def mount_array_disk(self, slot: str) -> Dict[str, Any]:
        """Mount an array disk.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MountArrayDisk($slot: String!) {
            mountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("mountArrayDisk", {}).get("success", False):
            message = result.get("mountArrayDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mount array disk: {message}")
        
        return result["mountArrayDisk"]
    
    async def unmount_array_disk(self, slot: str) -> Dict[str, Any]:
        """Unmount an array disk.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UnmountArrayDisk($slot: String!) {
            unmountArrayDisk(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("unmountArrayDisk", {}).get("success", False):
            message = result.get("unmountArrayDisk", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to unmount array disk: {message}")
        
        return result["unmountArrayDisk"]
    
    async def clear_array_disk_statistics(self, slot: str) -> Dict[str, Any]:
        """Clear array disk statistics.
        
        Args:
            slot: The disk slot (e.g., "disk1")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ClearArrayDiskStatistics($slot: String!) {
            clearArrayDiskStatistics(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("clearArrayDiskStatistics", {}).get("success", False):
            message = result.get("clearArrayDiskStatistics", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to clear array disk statistics: {message}")
        
        return result["clearArrayDiskStatistics"]
