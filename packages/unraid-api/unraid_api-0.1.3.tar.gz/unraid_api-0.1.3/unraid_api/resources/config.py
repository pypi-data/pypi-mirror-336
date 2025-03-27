"""Config resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class ConfigResource:
    """Config resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Config resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_system_config(self) -> Dict[str, Any]:
        """Get the system configuration.
        
        Returns:
            The system configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetSystemConfig {
            systemConfig {
                hostname
                description
                model
                version
                motherboard
                cpu {
                    model
                    cores
                    threads
                }
                memory {
                    total
                    used
                    free
                }
                network {
                    interfaces {
                        name
                        mac
                        ip
                        netmask
                        gateway
                        up
                        speed
                        duplex
                    }
                    dnsServers
                    hostname
                }
                display {
                    branding
                    theme
                    language
                }
                timezone
                notifications {
                    email {
                        enabled
                        to
                        from
                        server
                        port
                        secure
                        authType
                        username
                    }
                    pushover {
                        enabled
                        userKey
                        appKey
                    }
                    agents {
                        arrayStart
                        arrayStop
                        diskWarning
                        cpuWarning
                        memoryWarning
                        updateAvailable
                    }
                }
                vm {
                    enabled
                    isolatedCpuPinning
                    pciPassthrough
                }
                docker {
                    enabled
                    auto
                    image
                    privileged
                }
                shares {
                    enableNetbios
                    enableWsd
                    enableAvahi
                    localMaster
                    security
                }
                ftp {
                    enabled
                    port
                    allowReset
                    publicAccess
                }
                dynamicDns {
                    enabled
                    service
                    domain
                    username
                }
                tunable {
                    cacheDirectoryMethod
                    cacheNoCache
                    sharesMissingEnable
                    shareNfsEnable
                    shareNfsGuest
                    shareNfsSecure
                    shareAftpEnable
                    shareAftpPublicEnable
                    shareAftpSecure
                }
                updates {
                    auto
                    autoNerdpack
                    autoDocker
                    autoPlugins
                    autoCommunityApplications
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "systemConfig" not in result:
            raise APIError("Invalid response format: missing systemConfig field")
        
        return result["systemConfig"]
    
    def update_system_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update the system configuration.
        
        Args:
            config: The configuration changes
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateSystemConfig($input: SystemConfigInput!) {
            updateSystemConfig(input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "input": config
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("updateSystemConfig", {}).get("success", False):
            message = result.get("updateSystemConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update system config: {message}")
        
        return result["updateSystemConfig"]
    
    def get_share_config(self, name: str) -> Dict[str, Any]:
        """Get a share configuration.
        
        Args:
            name: The share name
            
        Returns:
            The share configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetShareConfig($name: String!) {
            shareConfig(name: $name) {
                name
                comment
                allocator
                fsType
                include
                exclude
                useCache
                exportEnabled
                security
                accessMode
                ownership
                diskIds
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = self.client.execute_query(query, variables)
        
        if "shareConfig" not in result:
            raise APIError("Invalid response format: missing shareConfig field")
        
        return result["shareConfig"]
    
    def update_share_config(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update a share configuration.
        
        Args:
            name: The share name
            config: The configuration changes
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateShareConfig($name: String!, $input: ShareConfigInput!) {
            updateShareConfig(name: $name, input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "input": config
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("updateShareConfig", {}).get("success", False):
            message = result.get("updateShareConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update share config: {message}")
        
        return result["updateShareConfig"]
    
    def create_share(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new share.
        
        Args:
            name: The share name
            config: The share configuration
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateShare($name: String!, $input: ShareConfigInput!) {
            createShare(name: $name, input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "input": config
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("createShare", {}).get("success", False):
            message = result.get("createShare", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create share: {message}")
        
        return result["createShare"]
    
    def delete_share(self, name: str) -> Dict[str, Any]:
        """Delete a share.
        
        Args:
            name: The share name
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteShare($name: String!) {
            deleteShare(name: $name) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("deleteShare", {}).get("success", False):
            message = result.get("deleteShare", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete share: {message}")
        
        return result["deleteShare"]
    
    def get_plugin_config(self, name: str) -> Dict[str, Any]:
        """Get a plugin configuration.
        
        Args:
            name: The plugin name
            
        Returns:
            The plugin configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetPluginConfig($name: String!) {
            pluginConfig(name: $name) {
                name
                version
                author
                description
                support
                icon
                settings
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = self.client.execute_query(query, variables)
        
        if "pluginConfig" not in result:
            raise APIError("Invalid response format: missing pluginConfig field")
        
        return result["pluginConfig"]
    
    def update_plugin_config(self, name: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update a plugin configuration.
        
        Args:
            name: The plugin name
            settings: The plugin settings
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdatePluginConfig($name: String!, $settings: JSONObject!) {
            updatePluginConfig(name: $name, settings: $settings) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "settings": settings
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("updatePluginConfig", {}).get("success", False):
            message = result.get("updatePluginConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update plugin config: {message}")
        
        return result["updatePluginConfig"]


class AsyncConfigResource:
    """Async Config resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Config resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_system_config(self) -> Dict[str, Any]:
        """Get the system configuration.
        
        Returns:
            The system configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetSystemConfig {
            systemConfig {
                hostname
                description
                model
                version
                motherboard
                cpu {
                    model
                    cores
                    threads
                }
                memory {
                    total
                    used
                    free
                }
                network {
                    interfaces {
                        name
                        mac
                        ip
                        netmask
                        gateway
                        up
                        speed
                        duplex
                    }
                    dnsServers
                    hostname
                }
                display {
                    branding
                    theme
                    language
                }
                timezone
                notifications {
                    email {
                        enabled
                        to
                        from
                        server
                        port
                        secure
                        authType
                        username
                    }
                    pushover {
                        enabled
                        userKey
                        appKey
                    }
                    agents {
                        arrayStart
                        arrayStop
                        diskWarning
                        cpuWarning
                        memoryWarning
                        updateAvailable
                    }
                }
                vm {
                    enabled
                    isolatedCpuPinning
                    pciPassthrough
                }
                docker {
                    enabled
                    auto
                    image
                    privileged
                }
                shares {
                    enableNetbios
                    enableWsd
                    enableAvahi
                    localMaster
                    security
                }
                ftp {
                    enabled
                    port
                    allowReset
                    publicAccess
                }
                dynamicDns {
                    enabled
                    service
                    domain
                    username
                }
                tunable {
                    cacheDirectoryMethod
                    cacheNoCache
                    sharesMissingEnable
                    shareNfsEnable
                    shareNfsGuest
                    shareNfsSecure
                    shareAftpEnable
                    shareAftpPublicEnable
                    shareAftpSecure
                }
                updates {
                    auto
                    autoNerdpack
                    autoDocker
                    autoPlugins
                    autoCommunityApplications
                }
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "systemConfig" not in result:
            raise APIError("Invalid response format: missing systemConfig field")
        
        return result["systemConfig"]
    
    async def update_system_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update the system configuration.
        
        Args:
            config: The configuration changes
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateSystemConfig($input: SystemConfigInput!) {
            updateSystemConfig(input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "input": config
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("updateSystemConfig", {}).get("success", False):
            message = result.get("updateSystemConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update system config: {message}")
        
        return result["updateSystemConfig"]
    
    async def get_share_config(self, name: str) -> Dict[str, Any]:
        """Get a share configuration.
        
        Args:
            name: The share name
            
        Returns:
            The share configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetShareConfig($name: String!) {
            shareConfig(name: $name) {
                name
                comment
                allocator
                fsType
                include
                exclude
                useCache
                exportEnabled
                security
                accessMode
                ownership
                diskIds
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "shareConfig" not in result:
            raise APIError("Invalid response format: missing shareConfig field")
        
        return result["shareConfig"]
    
    async def update_share_config(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update a share configuration.
        
        Args:
            name: The share name
            config: The configuration changes
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateShareConfig($name: String!, $input: ShareConfigInput!) {
            updateShareConfig(name: $name, input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "input": config
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("updateShareConfig", {}).get("success", False):
            message = result.get("updateShareConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update share config: {message}")
        
        return result["updateShareConfig"]
    
    async def create_share(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new share.
        
        Args:
            name: The share name
            config: The share configuration
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateShare($name: String!, $input: ShareConfigInput!) {
            createShare(name: $name, input: $input) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "input": config
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("createShare", {}).get("success", False):
            message = result.get("createShare", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create share: {message}")
        
        return result["createShare"]
    
    async def delete_share(self, name: str) -> Dict[str, Any]:
        """Delete a share.
        
        Args:
            name: The share name
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteShare($name: String!) {
            deleteShare(name: $name) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("deleteShare", {}).get("success", False):
            message = result.get("deleteShare", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete share: {message}")
        
        return result["deleteShare"]
    
    async def get_plugin_config(self, name: str) -> Dict[str, Any]:
        """Get a plugin configuration.
        
        Args:
            name: The plugin name
            
        Returns:
            The plugin configuration
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetPluginConfig($name: String!) {
            pluginConfig(name: $name) {
                name
                version
                author
                description
                support
                icon
                settings
            }
        }
        """
        
        variables = {
            "name": name
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "pluginConfig" not in result:
            raise APIError("Invalid response format: missing pluginConfig field")
        
        return result["pluginConfig"]
    
    async def update_plugin_config(self, name: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update a plugin configuration.
        
        Args:
            name: The plugin name
            settings: The plugin settings
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdatePluginConfig($name: String!, $settings: JSONObject!) {
            updatePluginConfig(name: $name, settings: $settings) {
                success
                message
            }
        }
        """
        
        variables = {
            "name": name,
            "settings": settings
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("updatePluginConfig", {}).get("success", False):
            message = result.get("updatePluginConfig", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update plugin config: {message}")
        
        return result["updatePluginConfig"]
