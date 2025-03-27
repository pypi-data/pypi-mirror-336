"""Docker resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class DockerResource:
    """Docker resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Docker resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_containers(self) -> List[Dict[str, Any]]:
        """Get all Docker containers.
        
        Returns:
            List of Docker containers
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDockerContainers {
            docker {
                containers {
                    id
                    names
                    image
                    state
                    status
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "docker" not in result or "containers" not in result["docker"]:
            raise APIError("Invalid response format: missing docker.containers field")
        
        return result["docker"]["containers"]
    
    def get_container(self, id: str) -> Dict[str, Any]:
        """Get a Docker container by ID.
        
        Args:
            id: The container ID
            
        Returns:
            The container info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetContainer($id: String!) {
            dockerContainer(id: $id) {
                id
                name
                image
                imageId
                status
                state
                created
                started
                finished
                exitCode
                autostart
                network
                repository
                command
                registry
                index
                nohc
                temp
                cpuPercent
                memUsage
                memLimit
                memPercent
                networkMode
                privileged
                restartPolicy
                logRotation
                ports {
                    IP
                    PrivatePort
                    PublicPort
                    Type
                }
                mounts {
                    name
                    source
                    destination
                    driver
                    mode
                    rw
                    propagation
                }
                icon
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(query, variables)
        
        if "dockerContainer" not in result:
            raise APIError("Invalid response format: missing dockerContainer field")
        
        return result["dockerContainer"]
    
    def start_container(self, id: str) -> Dict[str, Any]:
        """Start a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartContainer($id: String!) {
            startContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("startContainer", {}).get("success", False):
            message = result.get("startContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start container: {message}")
        
        return result["startContainer"]
    
    def stop_container(self, id: str) -> Dict[str, Any]:
        """Stop a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopContainer($id: String!) {
            stopContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("stopContainer", {}).get("success", False):
            message = result.get("stopContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop container: {message}")
        
        return result["stopContainer"]
    
    def restart_container(self, id: str) -> Dict[str, Any]:
        """Restart a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RestartContainer($id: String!) {
            restartContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("restartContainer", {}).get("success", False):
            message = result.get("restartContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to restart container: {message}")
        
        return result["restartContainer"]
    
    def remove_container(self, id: str) -> Dict[str, Any]:
        """Remove a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveContainer($id: String!) {
            removeContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("removeContainer", {}).get("success", False):
            message = result.get("removeContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove container: {message}")
        
        return result["removeContainer"]
    
    def get_container_logs(self, id: str, tail: Optional[int] = None) -> str:
        """Get Docker container logs.
        
        Args:
            id: The container ID
            tail: Number of lines to show from the end of the logs (default: None, show all)
            
        Returns:
            The container logs
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetContainerLogs($id: String!, $tail: Int) {
            containerLogs(id: $id, tail: $tail)
        }
        """
        
        variables = {
            "id": id
        }
        
        if tail is not None:
            variables["tail"] = tail
        
        result = self.client.execute_query(query, variables)
        
        if "containerLogs" not in result:
            raise APIError("Invalid response format: missing containerLogs field")
        
        return result["containerLogs"]
    
    def get_images(self) -> List[Dict[str, Any]]:
        """Get all Docker images.
        
        Returns:
            List of Docker images
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetImages {
            dockerImages {
                id
                name
                repository
                tag
                created
                size
                containers
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "dockerImages" not in result:
            raise APIError("Invalid response format: missing dockerImages field")
        
        return result["dockerImages"]
    
    def pull_image(self, repository: str, tag: str = "latest") -> Dict[str, Any]:
        """Pull a Docker image.
        
        Args:
            repository: The image repository
            tag: The image tag (default: "latest")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PullImage($repository: String!, $tag: String) {
            pullImage(repository: $repository, tag: $tag) {
                success
                message
            }
        }
        """
        
        variables = {
            "repository": repository,
            "tag": tag
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("pullImage", {}).get("success", False):
            message = result.get("pullImage", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pull image: {message}")
        
        return result["pullImage"]
    
    def remove_image(self, id: str) -> Dict[str, Any]:
        """Remove a Docker image.
        
        Args:
            id: The image ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveImage($id: String!) {
            removeImage(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("removeImage", {}).get("success", False):
            message = result.get("removeImage", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove image: {message}")
        
        return result["removeImage"]
    
    def get_networks(self) -> List[Dict[str, Any]]:
        """Get all Docker networks.
        
        Returns:
            List of Docker networks
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNetworks {
            dockerNetworks {
                id
                name
                driver
                scope
                subnet
                gateway
                containers
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "dockerNetworks" not in result:
            raise APIError("Invalid response format: missing dockerNetworks field")
        
        return result["dockerNetworks"]


class AsyncDockerResource:
    """Async Docker resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Docker resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_containers(self) -> List[Dict[str, Any]]:
        """Get all Docker containers.
        
        Returns:
            List of Docker containers
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetDockerContainers {
            docker {
                containers {
                    id
                    names
                    image
                    state
                    status
                }
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "docker" not in result or "containers" not in result["docker"]:
            raise APIError("Invalid response format: missing docker.containers field")
        
        return result["docker"]["containers"]
    
    async def get_container(self, id: str) -> Dict[str, Any]:
        """Get a Docker container by ID.
        
        Args:
            id: The container ID
            
        Returns:
            The container info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetContainer($id: String!) {
            dockerContainer(id: $id) {
                id
                name
                image
                imageId
                status
                state
                created
                started
                finished
                exitCode
                autostart
                network
                repository
                command
                registry
                index
                nohc
                temp
                cpuPercent
                memUsage
                memLimit
                memPercent
                networkMode
                privileged
                restartPolicy
                logRotation
                ports {
                    IP
                    PrivatePort
                    PublicPort
                    Type
                }
                mounts {
                    name
                    source
                    destination
                    driver
                    mode
                    rw
                    propagation
                }
                icon
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "dockerContainer" not in result:
            raise APIError("Invalid response format: missing dockerContainer field")
        
        return result["dockerContainer"]
    
    async def start_container(self, id: str) -> Dict[str, Any]:
        """Start a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StartContainer($id: String!) {
            startContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("startContainer", {}).get("success", False):
            message = result.get("startContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to start container: {message}")
        
        return result["startContainer"]
    
    async def stop_container(self, id: str) -> Dict[str, Any]:
        """Stop a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation StopContainer($id: String!) {
            stopContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("stopContainer", {}).get("success", False):
            message = result.get("stopContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to stop container: {message}")
        
        return result["stopContainer"]
    
    async def restart_container(self, id: str) -> Dict[str, Any]:
        """Restart a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RestartContainer($id: String!) {
            restartContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("restartContainer", {}).get("success", False):
            message = result.get("restartContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to restart container: {message}")
        
        return result["restartContainer"]
    
    async def remove_container(self, id: str) -> Dict[str, Any]:
        """Remove a Docker container.
        
        Args:
            id: The container ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveContainer($id: String!) {
            removeContainer(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("removeContainer", {}).get("success", False):
            message = result.get("removeContainer", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove container: {message}")
        
        return result["removeContainer"]
    
    async def get_container_logs(self, id: str, tail: Optional[int] = None) -> str:
        """Get Docker container logs.
        
        Args:
            id: The container ID
            tail: Number of lines to show from the end of the logs (default: None, show all)
            
        Returns:
            The container logs
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetContainerLogs($id: String!, $tail: Int) {
            containerLogs(id: $id, tail: $tail)
        }
        """
        
        variables = {
            "id": id
        }
        
        if tail is not None:
            variables["tail"] = tail
        
        result = await self.client.execute_query(query, variables)
        
        if "containerLogs" not in result:
            raise APIError("Invalid response format: missing containerLogs field")
        
        return result["containerLogs"]
    
    async def get_images(self) -> List[Dict[str, Any]]:
        """Get all Docker images.
        
        Returns:
            List of Docker images
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetImages {
            dockerImages {
                id
                name
                repository
                tag
                created
                size
                containers
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "dockerImages" not in result:
            raise APIError("Invalid response format: missing dockerImages field")
        
        return result["dockerImages"]
    
    async def pull_image(self, repository: str, tag: str = "latest") -> Dict[str, Any]:
        """Pull a Docker image.
        
        Args:
            repository: The image repository
            tag: The image tag (default: "latest")
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation PullImage($repository: String!, $tag: String) {
            pullImage(repository: $repository, tag: $tag) {
                success
                message
            }
        }
        """
        
        variables = {
            "repository": repository,
            "tag": tag
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("pullImage", {}).get("success", False):
            message = result.get("pullImage", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to pull image: {message}")
        
        return result["pullImage"]
    
    async def remove_image(self, id: str) -> Dict[str, Any]:
        """Remove a Docker image.
        
        Args:
            id: The image ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation RemoveImage($id: String!) {
            removeImage(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("removeImage", {}).get("success", False):
            message = result.get("removeImage", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to remove image: {message}")
        
        return result["removeImage"]
    
    async def get_networks(self) -> List[Dict[str, Any]]:
        """Get all Docker networks.
        
        Returns:
            List of Docker networks
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNetworks {
            dockerNetworks {
                id
                name
                driver
                scope
                subnet
                gateway
                containers
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "dockerNetworks" not in result:
            raise APIError("Invalid response format: missing dockerNetworks field")
        
        return result["dockerNetworks"]
