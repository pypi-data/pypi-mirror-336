"""Async client for the Unraid API."""
import logging
from typing import Any, Dict, List, Optional, TypeVar, Generic
import json

import httpx
import websockets
import websockets.exceptions
import asyncio

from .exceptions import (
    GraphQLError,
    ConnectionError,
    AuthenticationError,
    SubscriptionError,
)
from .auth import AuthManager
from .resources.array import AsyncArrayResource
from .resources.disk import AsyncDiskResource
from .resources.docker import AsyncDockerResource
from .resources.vm import AsyncVMResource
from .resources.info import AsyncInfoResource
from .resources.notification import AsyncNotificationResource

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AsyncUnraidClient:
    """Asynchronous client for the Unraid API."""

    def __init__(
        self,
        host: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
        verify_ssl: bool = False,
        api_key: Optional[str] = None,
    ):
        """Initialize the client.
        
        Args:
            host: The hostname or IP address of the Unraid server
            port: The port to connect to
            use_ssl: Whether to use SSL
            token_persistence_path: Path to save tokens for persistence
            verify_ssl: Whether to verify SSL certificates (default: False)
            api_key: API key for authentication (default: None)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.api_key = api_key
        self._auth_manager = AuthManager(
            host=host,
            port=port,
            use_ssl=use_ssl,
            token_persistence_path=token_persistence_path,
            verify_ssl=verify_ssl,
        )
        self._scheme = "https" if use_ssl else "http"
        self._base_url = f"{self._scheme}://{host}:{port}/graphql"
        self._ws_scheme = "wss" if use_ssl else "ws"
        self._ws_url = f"{self._ws_scheme}://{host}:{port}/graphql"
        self._http_client = httpx.AsyncClient(verify=verify_ssl)
        self.verify_ssl = verify_ssl
        
        # Initialize resources
        self.array = AsyncArrayResource(self)
        self.disk = AsyncDiskResource(self)
        self.docker = AsyncDockerResource(self)
        self.vm = AsyncVMResource(self)
        self.info = AsyncInfoResource(self)
        self.notification = AsyncNotificationResource(self)

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
        return self._auth_manager.login(username, password)

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
        return self._auth_manager.connect_sign_in(connect_token)

    async def logout(self) -> None:
        """Logout and clear tokens."""
        self._auth_manager.logout()

    async def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a GraphQL query.
        
        Args:
            query: The GraphQL query to execute
            variables: Variables to pass to the query
            
        Returns:
            The query result
            
        Raises:
            GraphQLError: If the query fails
            ConnectionError: If the server cannot be reached
            AuthenticationError: If authentication fails
        """
        headers = {}
        
        # Use API key if available
        if self.api_key:
            headers["x-api-key"] = self.api_key
        else:
            # Fall back to token-based auth
            try:
                auth_headers = self._auth_manager.get_auth_headers()
                headers.update(auth_headers)
            except AuthenticationError:
                raise AuthenticationError("Not authenticated")
        
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl) as client:
                response = await client.post(
                    self._base_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                errors = data["errors"]
                error_message = errors[0].get("message", "Unknown query error")
                raise GraphQLError(f"Query failed: {error_message}")
            
            return data["data"]
        
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication failed, token may be expired")
            raise ConnectionError(f"HTTP error: {e}")

    async def subscribe(self, subscription: str, variables: Optional[Dict[str, Any]] = None, callback=None):
        """Subscribe to a GraphQL subscription.
        
        Args:
            subscription: The GraphQL subscription query
            variables: Variables to pass to the subscription
            callback: Function to call with each update
            
        Yields:
            Subscription updates
            
        Raises:
            SubscriptionError: If the subscription fails
            ConnectionError: If the server cannot be reached
            AuthenticationError: If authentication fails
        """
        headers = self._auth_manager.get_auth_headers()
        auth_token = headers["Authorization"].split(" ")[1]
        
        payload = {
            "query": subscription,
            "variables": variables or {}
        }
        
        # Prepare the initial payload for subscription
        init_message = {
            "type": "connection_init",
            "payload": {"Authorization": f"Bearer {auth_token}"}
        }
        
        # Prepare the subscription payload
        subscription_id = 1
        subscribe_message = {
            "id": str(subscription_id),
            "type": "start",
            "payload": {
                "query": subscription,
                "variables": variables or {}
            }
        }
        
        try:
            async with websockets.connect(
                self._ws_url, 
                subprotocols=["graphql-ws"],
                ssl=None if not self.verify_ssl else True
            ) as websocket:
                # Send connection init
                await websocket.send(json.dumps(init_message))
                
                # Wait for connection_ack
                ack = await websocket.recv()
                ack_data = json.loads(ack)
                if ack_data.get("type") != "connection_ack":
                    raise SubscriptionError(f"Failed to establish subscription connection: {ack_data}")
                
                # Send subscription
                await websocket.send(json.dumps(subscribe_message))
                
                # Process incoming messages
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    message_type = data.get("type")
                    
                    if message_type == "error":
                        payload = data.get("payload", {})
                        error_message = payload.get("message", "Unknown subscription error")
                        raise SubscriptionError(f"Subscription error: {error_message}")
                    
                    if message_type == "complete":
                        logger.debug(f"Subscription {subscription_id} completed")
                        break
                    
                    if message_type == "data":
                        payload = data.get("payload", {})
                        if "errors" in payload:
                            errors = payload["errors"]
                            error_message = errors[0].get("message", "Unknown subscription error")
                            raise SubscriptionError(f"Subscription error: {error_message}")
                        
                        result = payload.get("data")
                        
                        if callback:
                            callback(result)
                        else:
                            yield result
        
        except websockets.exceptions.ConnectionClosed as e:
            raise ConnectionError(f"Subscription connection closed: {e}")
        except (ConnectionError, TimeoutError) as e:
            raise ConnectionError(f"Failed to establish subscription connection: {e}")

    async def close(self) -> None:
        """Close the client and release resources."""
        await self._http_client.aclose() 