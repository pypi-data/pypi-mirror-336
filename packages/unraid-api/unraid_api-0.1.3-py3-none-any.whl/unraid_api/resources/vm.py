"""VM resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class VMResource:
    """VM resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the VM resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_vms(self) -> Dict[str, Any]:
        """Get all VMs.
        
        Returns:
            Dictionary with VM information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMs {
            vms {
                domain {
                    uuid
                    name
                    state
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "vms" not in result:
            raise APIError("Invalid response format: missing vms field")
        
        return result["vms"]
    
    def get_vm(self, id: str) -> Dict[str, Any]:
        """Get a VM by ID.
        
        Args:
            id: The VM ID
            
        Returns:
            The VM info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVM($id: String!) {
            vm(id: $id) {
                id
                name
                coreCount
                thread
                memorySize
                status
                icon
                description
                primaryGPU
                autostart
                template
                disks {
                    name
                    size
                    driver
                    interface
                }
                nics {
                    name
                    mac
                    bridge
                }
                usbDevices {
                    name
                    id
                }
                usb {
                    enabled
                }
                sound {
                    enabled
                }
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(query, variables)
        
        if "vm" not in result:
            raise APIError("Invalid response format: missing vm field")
        
        return result["vm"]
    
    def start_vm(self, id: str) -> Dict[str, Any]:
        """Start a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartVM($id: String!) {
            startVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("startVM", {}).get("success", False):
            message = result.get("startVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start VM: {message}")
        
        return result["startVM"]
    
    def stop_vm(self, id: str) -> Dict[str, Any]:
        """Stop a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopVM($id: String!) {
            stopVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("stopVM", {}).get("success", False):
            message = result.get("stopVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop VM: {message}")
        
        return result["stopVM"]
    
    def force_stop_vm(self, id: str) -> Dict[str, Any]:
        """Force stop a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ForceStopVM($id: String!) {
            forceStopVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("forceStopVM", {}).get("success", False):
            message = result.get("forceStopVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to force stop VM: {message}")
        
        return result["forceStopVM"]
    
    def restart_vm(self, id: str) -> Dict[str, Any]:
        """Restart a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RestartVM($id: String!) {
            restartVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("restartVM", {}).get("success", False):
            message = result.get("restartVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to restart VM: {message}")
        
        return result["restartVM"]
    
    def pause_vm(self, id: str) -> Dict[str, Any]:
        """Pause a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PauseVM($id: String!) {
            pauseVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("pauseVM", {}).get("success", False):
            message = result.get("pauseVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pause VM: {message}")
        
        return result["pauseVM"]
    
    def resume_vm(self, id: str) -> Dict[str, Any]:
        """Resume a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ResumeVM($id: String!) {
            resumeVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("resumeVM", {}).get("success", False):
            message = result.get("resumeVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to resume VM: {message}")
        
        return result["resumeVM"]
    
    def get_vm_templates(self) -> List[Dict[str, Any]]:
        """Get all VM templates.
        
        Returns:
            List of VM templates
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMTemplates {
            vmTemplates {
                id
                name
                icon
                description
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "vmTemplates" not in result:
            raise APIError("Invalid response format: missing vmTemplates field")
        
        return result["vmTemplates"]
    
    def create_vm_from_template(self, template_id: str, name: str) -> Dict[str, Any]:
        """Create a VM from a template.
        
        Args:
            template_id: The template ID
            name: The name for the new VM
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateVMFromTemplate($templateId: String!, $name: String!) {
            createVMFromTemplate(templateId: $templateId, name: $name) {
                success
                message
            }
        }
        """
        
        variables = {
            "templateId": template_id,
            "name": name
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("createVMFromTemplate", {}).get("success", False):
            message = result.get("createVMFromTemplate", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create VM from template: {message}")
        
        return result["createVMFromTemplate"]
    
    def delete_vm(self, id: str) -> Dict[str, Any]:
        """Delete a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteVM($id: String!) {
            deleteVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("deleteVM", {}).get("success", False):
            message = result.get("deleteVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete VM: {message}")
        
        return result["deleteVM"]


class AsyncVMResource:
    """Async VM resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the VM resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_vms(self) -> Dict[str, Any]:
        """Get all VMs.
        
        Returns:
            Dictionary with VM information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMs {
            vms {
                domain {
                    uuid
                    name
                    state
                }
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "vms" not in result:
            raise APIError("Invalid response format: missing vms field")
        
        return result["vms"]
    
    async def get_vm(self, id: str) -> Dict[str, Any]:
        """Get a VM by ID.
        
        Args:
            id: The VM ID
            
        Returns:
            The VM info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVM($id: String!) {
            vm(id: $id) {
                id
                name
                coreCount
                thread
                memorySize
                status
                icon
                description
                primaryGPU
                autostart
                template
                disks {
                    name
                    size
                    driver
                    interface
                }
                nics {
                    name
                    mac
                    bridge
                }
                usbDevices {
                    name
                    id
                }
                usb {
                    enabled
                }
                sound {
                    enabled
                }
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "vm" not in result:
            raise APIError("Invalid response format: missing vm field")
        
        return result["vm"]
    
    async def start_vm(self, id: str) -> Dict[str, Any]:
        """Start a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartVM($id: String!) {
            startVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("startVM", {}).get("success", False):
            message = result.get("startVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start VM: {message}")
        
        return result["startVM"]
    
    async def stop_vm(self, id: str) -> Dict[str, Any]:
        """Stop a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopVM($id: String!) {
            stopVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("stopVM", {}).get("success", False):
            message = result.get("stopVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop VM: {message}")
        
        return result["stopVM"]
    
    async def force_stop_vm(self, id: str) -> Dict[str, Any]:
        """Force stop a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ForceStopVM($id: String!) {
            forceStopVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("forceStopVM", {}).get("success", False):
            message = result.get("forceStopVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to force stop VM: {message}")
        
        return result["forceStopVM"]
    
    async def restart_vm(self, id: str) -> Dict[str, Any]:
        """Restart a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RestartVM($id: String!) {
            restartVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("restartVM", {}).get("success", False):
            message = result.get("restartVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to restart VM: {message}")
        
        return result["restartVM"]
    
    async def pause_vm(self, id: str) -> Dict[str, Any]:
        """Pause a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PauseVM($id: String!) {
            pauseVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("pauseVM", {}).get("success", False):
            message = result.get("pauseVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pause VM: {message}")
        
        return result["pauseVM"]
    
    async def resume_vm(self, id: str) -> Dict[str, Any]:
        """Resume a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ResumeVM($id: String!) {
            resumeVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("resumeVM", {}).get("success", False):
            message = result.get("resumeVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to resume VM: {message}")
        
        return result["resumeVM"]
    
    async def get_vm_templates(self) -> List[Dict[str, Any]]:
        """Get all VM templates.
        
        Returns:
            List of VM templates
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetVMTemplates {
            vmTemplates {
                id
                name
                icon
                description
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "vmTemplates" not in result:
            raise APIError("Invalid response format: missing vmTemplates field")
        
        return result["vmTemplates"]
    
    async def create_vm_from_template(self, template_id: str, name: str) -> Dict[str, Any]:
        """Create a VM from a template.
        
        Args:
            template_id: The template ID
            name: The name for the new VM
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateVMFromTemplate($templateId: String!, $name: String!) {
            createVMFromTemplate(templateId: $templateId, name: $name) {
                success
                message
            }
        }
        """
        
        variables = {
            "templateId": template_id,
            "name": name
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("createVMFromTemplate", {}).get("success", False):
            message = result.get("createVMFromTemplate", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create VM from template: {message}")
        
        return result["createVMFromTemplate"]
    
    async def delete_vm(self, id: str) -> Dict[str, Any]:
        """Delete a VM.
        
        Args:
            id: The VM ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteVM($id: String!) {
            deleteVM(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("deleteVM", {}).get("success", False):
            message = result.get("deleteVM", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete VM: {message}")
        
        return result["deleteVM"]
