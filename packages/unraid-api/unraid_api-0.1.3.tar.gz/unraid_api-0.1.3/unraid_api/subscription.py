"""Subscription module for unraid_api."""
import asyncio
import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union

import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from .exceptions import AuthenticationError, ConnectionError, SubscriptionError

logger = logging.getLogger(__name__)


class Subscription:
    """GraphQL subscription client for real-time data updates from Unraid."""
    
    def __init__(
        self,
        client,
        subscription_query: str,
        variables: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ):
        """Initialize a GraphQL subscription.
        
        Args:
            client: The Unraid client (sync or async)
            subscription_query: The GraphQL subscription query
            variables: Variables for the subscription (default: None)
            callback: Callback function for data updates (default: None)
        """
        self.client = client
        self.subscription_query = subscription_query
        self.variables = variables or {}
        self.callback = callback
        self._ws = None
        self._task = None
        self._running = False
        self._reconnect_delay = 1  # Initial reconnect delay in seconds
        self._max_reconnect_delay = 60  # Maximum reconnect delay in seconds
    
    async def start(self) -> None:
        """Start the subscription.
        
        Raises:
            AuthenticationError: If not authenticated
            ConnectionError: If the server cannot be reached
            SubscriptionError: If the subscription fails
        """
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._subscription_handler())
    
    async def stop(self) -> None:
        """Stop the subscription."""
        self._running = False
        
        if self._ws:
            await self._ws.close()
            self._ws = None
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
    
    async def _subscription_handler(self) -> None:
        """Internal subscription handler."""
        while self._running:
            try:
                # Get a valid authentication token
                if hasattr(self.client.auth, "get_access_token"):
                    # Async client
                    token = await self.client.auth.get_access_token()
                else:
                    # Sync client
                    token = self.client.auth.get_access_token()
                
                # Build the WebSocket URL
                ws_protocol = "wss" if self.client.use_ssl else "ws"
                ws_url = f"{ws_protocol}://{self.client.host}:{self.client.port}/graphql"
                
                # Prepare the subscription message
                init_message = {
                    "type": "connection_init",
                    "payload": {"Authorization": f"Bearer {token}"}
                }
                
                subscription_message = {
                    "id": "1",
                    "type": "start",
                    "payload": {
                        "query": self.subscription_query,
                        "variables": self.variables
                    }
                }
                
                # Connect to the WebSocket
                async with websockets.connect(ws_url) as websocket:
                    self._ws = websocket
                    self._reconnect_delay = 1  # Reset reconnect delay on successful connection
                    
                    # Send the initialization message
                    await websocket.send(json.dumps(init_message))
                    
                    # Wait for acknowledgement
                    ack = await websocket.recv()
                    ack_data = json.loads(ack)
                    
                    if ack_data.get("type") != "connection_ack":
                        raise SubscriptionError(f"Failed to initialize subscription: {ack_data}")
                    
                    # Send the subscription message
                    await websocket.send(json.dumps(subscription_message))
                    
                    # Process incoming messages
                    while self._running:
                        try:
                            message = await websocket.recv()
                            data = json.loads(message)
                            
                            if data.get("type") == "error":
                                logger.error(f"Subscription error: {data.get('payload')}")
                                # Don't raise an exception, just log and continue
                                
                            elif data.get("type") == "data":
                                payload = data.get("payload", {})
                                if self.callback and "data" in payload:
                                    await self._call_callback(payload["data"])
                                    
                            elif data.get("type") == "complete":
                                logger.info("Subscription completed by server")
                                break
                                
                        except ConnectionClosedOK:
                            logger.info("Subscription connection closed normally")
                            break
                            
                        except ConnectionClosedError as e:
                            logger.warning(f"Subscription connection closed unexpectedly: {e}")
                            break
                            
            except AuthenticationError as e:
                logger.error(f"Authentication error in subscription: {e}")
                break  # Don't retry on auth errors
                
            except (ConnectionError, Exception) as e:
                if not self._running:
                    break
                
                logger.warning(f"Subscription error, will retry in {self._reconnect_delay}s: {e}")
                
                # Wait before reconnecting
                await asyncio.sleep(self._reconnect_delay)
                
                # Exponential backoff with max delay
                self._reconnect_delay = min(self._reconnect_delay * 2, self._max_reconnect_delay)
    
    async def _call_callback(self, data: Dict[str, Any]) -> None:
        """Call the callback function with the subscription data.
        
        Args:
            data: The subscription data
        """
        if not self.callback:
            return
        
        try:
            # Check if the callback is a coroutine function
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(data)
            else:
                self.callback(data)
        except Exception as e:
            logger.error(f"Error in subscription callback: {e}")


class SubscriptionManager:
    """Manager for GraphQL subscriptions."""
    
    def __init__(self, client):
        """Initialize the subscription manager.
        
        Args:
            client: The Unraid client (sync or async)
        """
        self.client = client
        self.subscriptions = {}
    
    async def subscribe(
        self,
        name: str,
        subscription_query: str,
        variables: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> None:
        """Create and start a subscription.
        
        Args:
            name: A unique name for the subscription
            subscription_query: The GraphQL subscription query
            variables: Variables for the subscription (default: None)
            callback: Callback function for data updates (default: None)
            
        Raises:
            ValueError: If a subscription with the same name already exists
            AuthenticationError: If not authenticated
            ConnectionError: If the server cannot be reached
            SubscriptionError: If the subscription fails
        """
        if name in self.subscriptions:
            raise ValueError(f"Subscription '{name}' already exists")
        
        subscription = Subscription(
            self.client, subscription_query, variables, callback
        )
        self.subscriptions[name] = subscription
        await subscription.start()
    
    async def unsubscribe(self, name: str) -> None:
        """Stop and remove a subscription.
        
        Args:
            name: The name of the subscription to stop
            
        Raises:
            ValueError: If the subscription does not exist
        """
        if name not in self.subscriptions:
            raise ValueError(f"Subscription '{name}' does not exist")
        
        await self.subscriptions[name].stop()
        del self.subscriptions[name]
    
    async def stop_all(self) -> None:
        """Stop all subscriptions."""
        for name in list(self.subscriptions.keys()):
            await self.subscriptions[name].stop()
        self.subscriptions.clear()
    
    def get_subscription(self, name: str) -> Subscription:
        """Get a subscription by name.
        
        Args:
            name: The name of the subscription
            
        Returns:
            The subscription
            
        Raises:
            ValueError: If the subscription does not exist
        """
        if name not in self.subscriptions:
            raise ValueError(f"Subscription '{name}' does not exist")
        
        return self.subscriptions[name]
