"""Asynchronous client for the Unraid GraphQL API."""
import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Union

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
    TokenExpiredError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class AsyncAuthManager:
    """Handles authentication and token management for Unraid GraphQL API."""

    def __init__(
        self,
        host: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
    ):
        """Initialize the authentication manager.
        
        Args:
            host: The hostname or IP address of the Unraid server
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            token_persistence_path: Path to save tokens for persistence (default: None)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.token_persistence_path = token_persistence_path
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expiry: Optional[int] = None
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"
        self._lock = asyncio.Lock()
        
        # Load persisted tokens if available
        if token_persistence_path:
            self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from the persistence path if available."""
        if not self.token_persistence_path:
            return
        
        try:
            with open(self.token_persistence_path, "r") as f:
                token_data = json.load(f)
                self._access_token = token_data.get("access_token")
                self._refresh_token = token_data.get("refresh_token")
                self._token_expiry = token_data.get("expiry")
                
                # Check if token is expired
                if self._token_expiry and self._token_expiry < time.time():
                    logger.info("Loaded token is expired, will need to refresh")
        except (FileNotFoundError, json.JSONDecodeError):
            logger.debug("No persisted tokens found or invalid token file")
    
    async def _save_tokens(self) -> None:
        """Save tokens to the persistence path if configured."""
        if not self.token_persistence_path:
            return
        
        token_data = {
            "access_token": self._access_token,
            "refresh_token": self._refresh_token,
            "expiry": self._token_expiry
        }
        
        try:
            with open(self.token_persistence_path, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            logger.warning(f"Failed to persist tokens: {e}")
    
    async def login(self, username: str, password: str) -> str:
        """Login to the Unraid server and get an authentication token.
        
        Args:
            username: The username to authenticate with
            password: The password to authenticate with
            
        Returns:
            The access token
            
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If the server cannot be reached
        """
        async with self._lock:  # Make sure only one auth operation happens at a time
            mutation = """
            mutation Login($username: String!, $password: String!) {
                login(username: $username, password: $password) {
                    accessToken
                    refreshToken
                    expiresIn
                }
            }
            """
            
            variables = {
                "username": username,
                "password": password
            }
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self._base_url,
                        json={"query": mutation, "variables": variables},
                        timeout=10.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    if "errors" in data:
                        errors = data["errors"]
                        error_message = errors[0].get("message", "Unknown authentication error")
                        raise AuthenticationError(f"Login failed: {error_message}")
                    
                    if "data" not in data or "login" not in data["data"]:
                        raise AuthenticationError("Invalid response format during login")
                    
                    login_data = data["data"]["login"]
                    self._access_token = login_data["accessToken"]
                    self._refresh_token = login_data["refreshToken"]
                    expires_in = login_data["expiresIn"]
                    self._token_expiry = int(time.time() + expires_in)
                    
                    # Save tokens if persistence is enabled
                    await self._save_tokens()
                    
                    return self._access_token
                    
            except httpx.RequestError as e:
                raise ConnectionError(f"Failed to connect to Unraid server: {e}")
            except httpx.HTTPStatusError as e:
                raise AuthenticationError(f"HTTP error during login: {e}")
    
    async def connect_sign_in(self, connect_token: str) -> str:
        """Sign in using Unraid Connect token.
        
        Args:
            connect_token: The Unraid Connect token
            
        Returns:
            The access token
            
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If the server cannot be reached
        """
        async with self._lock:
            mutation = """
            mutation ConnectSignIn($token: String!) {
                connectSignIn(token: $token) {
                    accessToken
                    refreshToken
                    expiresIn
                }
            }
            """
            
            variables = {
                "token": connect_token
            }
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self._base_url,
                        json={"query": mutation, "variables": variables},
                        timeout=10.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    if "errors" in data:
                        errors = data["errors"]
                        error_message = errors[0].get("message", "Unknown authentication error")
                        raise AuthenticationError(f"Connect sign-in failed: {error_message}")
                    
                    if "data" not in data or "connectSignIn" not in data["data"]:
                        raise AuthenticationError("Invalid response format during connect sign-in")
                    
                    login_data = data["data"]["connectSignIn"]
                    self._access_token = login_data["accessToken"]
                    self._refresh_token = login_data["refreshToken"]
                    expires_in = login_data["expiresIn"]
                    self._token_expiry = int(time.time() + expires_in)
                    
                    # Save tokens if persistence is enabled
                    await self._save_tokens()
                    
                    return self._access_token
                    
            except httpx.RequestError as e:
                raise ConnectionError(f"Failed to connect to Unraid server: {e}")
            except httpx.HTTPStatusError as e:
                raise AuthenticationError(f"HTTP error during connect sign-in: {e}")
    
    async def refresh_token(self) -> str:
        """Refresh the access token using the refresh token.
        
        Returns:
            The new access token
            
        Raises:
            TokenExpiredError: If the refresh token is expired or invalid
            ConnectionError: If the server cannot be reached
        """
        async with self._lock:
            if not self._refresh_token:
                raise TokenExpiredError("No refresh token available")
            
            mutation = """
            mutation RefreshToken($refreshToken: String!) {
                refreshToken(refreshToken: $refreshToken) {
                    accessToken
                    refreshToken
                    expiresIn
                }
            }
            """
            
            variables = {
                "refreshToken": self._refresh_token
            }
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self._base_url,
                        json={"query": mutation, "variables": variables},
                        timeout=10.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    if "errors" in data:
                        errors = data["errors"]
                        error_message = errors[0].get("message", "Unknown token refresh error")
                        raise TokenExpiredError(f"Token refresh failed: {error_message}")
                    
                    if "data" not in data or "refreshToken" not in data["data"]:
                        raise TokenExpiredError("Invalid response format during token refresh")
                    
                    token_data = data["data"]["refreshToken"]
                    self._access_token = token_data["accessToken"]
                    self._refresh_token = token_data["refreshToken"]
                    expires_in = token_data["expiresIn"]
                    self._token_expiry = int(time.time() + expires_in)
                    
                    # Save tokens if persistence is enabled
                    await self._save_tokens()
                    
                    return self._access_token
                    
            except httpx.RequestError as e:
                raise ConnectionError(f"Failed to connect to Unraid server: {e}")
            except httpx.HTTPStatusError as e:
                raise TokenExpiredError(f"HTTP error during token refresh: {e}")
    
    async def get_access_token(self) -> str:
        """Get the current access token, refreshing if necessary.
        
        Returns:
            The access token
            
        Raises:
            AuthenticationError: If no authentication has been performed
            TokenExpiredError: If the token is expired and cannot be refreshed
        """
        if not self._access_token:
            raise AuthenticationError("Not authenticated")
        
        # Check if token is expired and needs refresh
        if self._token_expiry and self._token_expiry < time.time() + 60:  # 60s buffer
            logger.debug("Access token is expired or about to expire, refreshing")
            return await self.refresh_token()
        
        return self._access_token
    
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated with a valid token.
        
        Returns:
            True if authenticated, False otherwise
        """
        if not self._access_token or not self._token_expiry:
            return False
        
        return self._token_expiry > time.time()
    
    async def logout(self) -> None:
        """Clear authentication tokens."""
        async with self._lock:
            self._access_token = None
            self._refresh_token = None
            self._token_expiry = None
            
            # Remove persisted tokens
            if self.token_persistence_path:
                try:
                    with open(self.token_persistence_path, "w") as f:
                        json.dump({}, f)
                except Exception as e:
                    logger.warning(f"Failed to clear persisted tokens: {e}")
    
    async def get_auth_headers(self) -> Dict[str, str]:
        """Get the authorization headers for API requests.
        
        Returns:
            Dict with authorization headers
            
        Raises:
            AuthenticationError: If not authenticated
        """
        token = await self.get_access_token()
        return {"Authorization": f"Bearer {token}"}


class AsyncUnraidClient:
    """Asynchronous client for the Unraid GraphQL API."""
    
    def __init__(
        self,
        host: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """Initialize the Unraid client.
        
        Args:
            host: The hostname or IP address of the Unraid server
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            token_persistence_path: Path to save tokens for persistence (default: None)
            timeout: Timeout for HTTP requests in seconds (default: 30.0)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.timeout = timeout
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"
        
        # Initialize authentication manager
        self.auth = AsyncAuthManager(host, port, use_ssl, token_persistence_path)
        
        # Resource clients will be initialized in the get_resource method
        self._resources = {}
    
    async def login(self, username: str, password: str) -> None:
        """Login to the Unraid server.
        
        Args:
            username: The username to authenticate with
            password: The password to authenticate with
            
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If the server cannot be reached
        """
        await self.auth.login(username, password)
    
    async def connect_sign_in(self, connect_token: str) -> None:
        """Sign in using Unraid Connect token.
        
        Args:
            connect_token: The Unraid Connect token
            
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If the server cannot be reached
        """
        await self.auth.connect_sign_in(connect_token)
    
    async def logout(self) -> None:
        """Logout and clear authentication tokens."""
        await self.auth.logout()
    
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.auth.is_authenticated()
    
    async def execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query.
        
        Args:
            query: The GraphQL query or mutation
            variables: Variables for the query (default: None)
            
        Returns:
            The query response data
            
        Raises:
            AuthenticationError: If not authenticated
            GraphQLError: If a GraphQL error occurs
            ConnectionError: If the server cannot be reached
            APIError: If the API returns an error
        """
        if variables is None:
            variables = {}
        
        try:
            headers = await self.auth.get_auth_headers()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._base_url,
                    json={"query": query, "variables": variables},
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                
                if "errors" in data:
                    errors = data["errors"]
                    error_message = errors[0].get("message", "Unknown GraphQL error")
                    raise GraphQLError(error_message, errors)
                
                if "data" not in data:
                    raise APIError("Invalid response format: missing data field")
                
                return data["data"]
                
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication required")
            raise APIError(f"HTTP error: {e}")
        except Exception as e:
            if isinstance(e, (GraphQLError, ConnectionError, AuthenticationError, APIError)):
                raise
            raise APIError(f"Unexpected error: {e}")
    
    def get_resource(self, resource_type: str):
        """Get a resource client.
        
        Args:
            resource_type: The type of resource to get
            
        Returns:
            The resource client
        """
        if resource_type not in self._resources:
            # Import the correct resource class on demand to avoid circular imports
            if resource_type == "array":
                from .resources.array import AsyncArrayResource
                self._resources[resource_type] = AsyncArrayResource(self)
            elif resource_type == "disk":
                from .resources.disk import AsyncDiskResource
                self._resources[resource_type] = AsyncDiskResource(self)
            elif resource_type == "docker":
                from .resources.docker import AsyncDockerResource
                self._resources[resource_type] = AsyncDockerResource(self)
            elif resource_type == "vm":
                from .resources.vm import AsyncVMResource
                self._resources[resource_type] = AsyncVMResource(self)
            elif resource_type == "notification":
                from .resources.notification import AsyncNotificationResource
                self._resources[resource_type] = AsyncNotificationResource(self)
            elif resource_type == "user":
                from .resources.user import AsyncUserResource
                self._resources[resource_type] = AsyncUserResource(self)
            elif resource_type == "info":
                from .resources.info import AsyncInfoResource
                self._resources[resource_type] = AsyncInfoResource(self)
            elif resource_type == "config":
                from .resources.config import AsyncConfigResource
                self._resources[resource_type] = AsyncConfigResource(self)
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")
        
        return self._resources[resource_type]
    
    @property
    def array(self):
        """Get the array resource client."""
        return self.get_resource("array")
    
    @property
    def disk(self):
        """Get the disk resource client."""
        return self.get_resource("disk")
    
    @property
    def docker(self):
        """Get the docker resource client."""
        return self.get_resource("docker")
    
    @property
    def vm(self):
        """Get the VM resource client."""
        return self.get_resource("vm")
    
    @property
    def notification(self):
        """Get the notification resource client."""
        return self.get_resource("notification")
    
    @property
    def user(self):
        """Get the user resource client."""
        return self.get_resource("user")
    
    @property
    def info(self):
        """Get the info resource client."""
        return self.get_resource("info")
    
    @property
    def config(self):
        """Get the config resource client."""
        return self.get_resource("config")
    
    # Convenience methods
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information.
        
        Returns:
            System information
            
        Raises:
            Various exceptions from execute_query
        """
        return await self.info.get_system_info()
    
    async def start_array(self) -> Dict[str, Any]:
        """Start the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        return await self.array.start_array()
    
    async def stop_array(self) -> Dict[str, Any]:
        """Stop the array.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        return await self.array.stop_array()
    
    async def reboot(self) -> Dict[str, Any]:
        """Reboot the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        return await self.info.reboot()
    
    async def shutdown(self) -> Dict[str, Any]:
        """Shutdown the Unraid server.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        return await self.info.shutdown()
