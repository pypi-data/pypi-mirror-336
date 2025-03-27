"""Array resource for pyunraid."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class ArrayResource:
    """Array resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the array resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def start_array(self) -> Dict[str, Any]:
        """Start the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartArray {
            startArray {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("startArray", {}).get("success", False):
            message = result.get("startArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start array: {message}")
        
        return result["startArray"]
    
    def stop_array(self) -> Dict[str, Any]:
        """Stop the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopArray {
            stopArray {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("stopArray", {}).get("success", False):
            message = result.get("stopArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop array: {message}")
        
        return result["stopArray"]
    
    def get_array_status(self) -> Dict[str, Any]:
        """Get the array status.
        
        Returns:
            The array status
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetArrayStatus {
            array {
                state
                capacity {
                    kilobytes {
                        free
                        used
                        total
                    }
                }
                parities {
                    id
                    size
                    status
                }
                disks {
                    id
                    size
                    status
                }
                caches {
                    id
                    size
                    status
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "array" not in result:
            raise APIError("Invalid response format: missing array field")
        
        return result["array"]
    
    def add_disk_to_array(self, slot: str, device: str) -> Dict[str, Any]:
        """Add a disk to the array.
        
        Args:
            slot: The slot to add the disk to (e.g., "disk1", "parity")
            device: The device to add (e.g., "/dev/sdb")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation AddDiskToArray($slot: String!, $device: String!) {
            addDiskToArray(slot: $slot, device: $device) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot,
            "device": device
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("addDiskToArray", {}).get("success", False):
            message = result.get("addDiskToArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to add disk to array: {message}")
        
        return result["addDiskToArray"]
    
    def remove_disk_from_array(self, slot: str) -> Dict[str, Any]:
        """Remove a disk from the array.
        
        Args:
            slot: The slot to remove the disk from (e.g., "disk1", "parity")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveDiskFromArray($slot: String!) {
            removeDiskFromArray(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("removeDiskFromArray", {}).get("success", False):
            message = result.get("removeDiskFromArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove disk from array: {message}")
        
        return result["removeDiskFromArray"]
    
    def start_parity_check(self, correcting: bool = True) -> Dict[str, Any]:
        """Start a parity check.
        
        Args:
            correcting: Whether to correct errors (default: True)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartParityCheck($correcting: Boolean) {
            startParityCheck(correcting: $correcting) {
                success
                message
            }
        }
        """
        
        variables = {
            "correcting": correcting
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("startParityCheck", {}).get("success", False):
            message = result.get("startParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start parity check: {message}")
        
        return result["startParityCheck"]
    
    def pause_parity_check(self) -> Dict[str, Any]:
        """Pause an ongoing parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PauseParityCheck {
            pauseParityCheck {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("pauseParityCheck", {}).get("success", False):
            message = result.get("pauseParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pause parity check: {message}")
        
        return result["pauseParityCheck"]
    
    def resume_parity_check(self) -> Dict[str, Any]:
        """Resume a paused parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ResumeParityCheck {
            resumeParityCheck {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("resumeParityCheck", {}).get("success", False):
            message = result.get("resumeParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to resume parity check: {message}")
        
        return result["resumeParityCheck"]
    
    def cancel_parity_check(self) -> Dict[str, Any]:
        """Cancel an ongoing parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CancelParityCheck {
            cancelParityCheck {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("cancelParityCheck", {}).get("success", False):
            message = result.get("cancelParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to cancel parity check: {message}")
        
        return result["cancelParityCheck"]
    
    def get_parity_history(self) -> List[Dict[str, Any]]:
        """Get the parity check history.
        
        Returns:
            The parity check history
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetParityHistory {
            parityHistory {
                duration
                speed
                status
                errors
                date
                corrected
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "parityHistory" not in result:
            raise APIError("Invalid response format: missing parityHistory field")
        
        return result["parityHistory"]


class AsyncArrayResource:
    """Async array resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the array resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def start_array(self) -> Dict[str, Any]:
        """Start the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartArray {
            startArray {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("startArray", {}).get("success", False):
            message = result.get("startArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start array: {message}")
        
        return result["startArray"]
    
    async def stop_array(self) -> Dict[str, Any]:
        """Stop the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopArray {
            stopArray {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("stopArray", {}).get("success", False):
            message = result.get("stopArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop array: {message}")
        
        return result["stopArray"]
    
    async def get_array_status(self) -> Dict[str, Any]:
        """Get the array status.
        
        Returns:
            The array status
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetArrayStatus {
            array {
                state
                capacity {
                    kilobytes {
                        free
                        used
                        total
                    }
                }
                parities {
                    id
                    size
                    status
                }
                disks {
                    id
                    size
                    status
                }
                caches {
                    id
                    size
                    status
                }
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "array" not in result:
            raise APIError("Invalid response format: missing array field")
        
        return result["array"]
    
    async def add_disk_to_array(self, slot: str, device: str) -> Dict[str, Any]:
        """Add a disk to the array.
        
        Args:
            slot: The slot to add the disk to (e.g., "disk1", "parity")
            device: The device to add (e.g., "/dev/sdb")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation AddDiskToArray($slot: String!, $device: String!) {
            addDiskToArray(slot: $slot, device: $device) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot,
            "device": device
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("addDiskToArray", {}).get("success", False):
            message = result.get("addDiskToArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to add disk to array: {message}")
        
        return result["addDiskToArray"]
    
    async def remove_disk_from_array(self, slot: str) -> Dict[str, Any]:
        """Remove a disk from the array.
        
        Args:
            slot: The slot to remove the disk from (e.g., "disk1", "parity")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveDiskFromArray($slot: String!) {
            removeDiskFromArray(slot: $slot) {
                success
                message
            }
        }
        """
        
        variables = {
            "slot": slot
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("removeDiskFromArray", {}).get("success", False):
            message = result.get("removeDiskFromArray", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove disk from array: {message}")
        
        return result["removeDiskFromArray"]
    
    async def start_parity_check(self, correcting: bool = True) -> Dict[str, Any]:
        """Start a parity check.
        
        Args:
            correcting: Whether to correct errors (default: True)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartParityCheck($correcting: Boolean) {
            startParityCheck(correcting: $correcting) {
                success
                message
            }
        }
        """
        
        variables = {
            "correcting": correcting
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("startParityCheck", {}).get("success", False):
            message = result.get("startParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start parity check: {message}")
        
        return result["startParityCheck"]
    
    async def pause_parity_check(self) -> Dict[str, Any]:
        """Pause an ongoing parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PauseParityCheck {
            pauseParityCheck {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("pauseParityCheck", {}).get("success", False):
            message = result.get("pauseParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pause parity check: {message}")
        
        return result["pauseParityCheck"]
    
    async def resume_parity_check(self) -> Dict[str, Any]:
        """Resume a paused parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ResumeParityCheck {
            resumeParityCheck {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("resumeParityCheck", {}).get("success", False):
            message = result.get("resumeParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to resume parity check: {message}")
        
        return result["resumeParityCheck"]
    
    async def cancel_parity_check(self) -> Dict[str, Any]:
        """Cancel an ongoing parity check.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CancelParityCheck {
            cancelParityCheck {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("cancelParityCheck", {}).get("success", False):
            message = result.get("cancelParityCheck", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to cancel parity check: {message}")
        
        return result["cancelParityCheck"]
    
    async def get_parity_history(self) -> List[Dict[str, Any]]:
        """Get the parity check history.
        
        Returns:
            The parity check history
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetParityHistory {
            parityHistory {
                duration
                speed
                status
                errors
                date
                corrected
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "parityHistory" not in result:
            raise APIError("Invalid response format: missing parityHistory field")
        
        return result["parityHistory"]
