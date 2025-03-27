"""Notification resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class NotificationResource:
    """Notification resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Notification resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_notifications(self) -> Dict[str, Any]:
        """Get notifications.
        
        Returns:
            Dictionary with notifications information
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNotifications {
            notifications {
                overview {
                    unread {
                        info
                        warning
                        alert
                        total
                    }
                }
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "notifications" not in result:
            raise APIError("Invalid response format: missing notifications field")
        
        return result["notifications"]
    
    def get_notification(self, id: str) -> Dict[str, Any]:
        """Get a notification by ID.
        
        Args:
            id: The notification ID
            
        Returns:
            The notification info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNotification($id: String!) {
            notification(id: $id) {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(query, variables)
        
        if "notification" not in result:
            raise APIError("Invalid response format: missing notification field")
        
        return result["notification"]
    
    def mark_notification_read(self, id: str) -> Dict[str, Any]:
        """Mark a notification as read.
        
        Args:
            id: The notification ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MarkNotificationRead($id: String!) {
            markNotificationRead(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("markNotificationRead", {}).get("success", False):
            message = result.get("markNotificationRead", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mark notification as read: {message}")
        
        return result["markNotificationRead"]
    
    def mark_all_notifications_read(self) -> Dict[str, Any]:
        """Mark all notifications as read.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MarkAllNotificationsRead {
            markAllNotificationsRead {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("markAllNotificationsRead", {}).get("success", False):
            message = result.get("markAllNotificationsRead", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mark all notifications as read: {message}")
        
        return result["markAllNotificationsRead"]
    
    def dismiss_notification(self, id: str) -> Dict[str, Any]:
        """Dismiss a notification.
        
        Args:
            id: The notification ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DismissNotification($id: String!) {
            dismissNotification(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("dismissNotification", {}).get("success", False):
            message = result.get("dismissNotification", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to dismiss notification: {message}")
        
        return result["dismissNotification"]
    
    def dismiss_all_notifications(self) -> Dict[str, Any]:
        """Dismiss all notifications.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DismissAllNotifications {
            dismissAllNotifications {
                success
                message
            }
        }
        """
        
        result = self.client.execute_query(mutation)
        
        if not result.get("dismissAllNotifications", {}).get("success", False):
            message = result.get("dismissAllNotifications", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to dismiss all notifications: {message}")
        
        return result["dismissAllNotifications"]
    
    def subscribe_to_notifications(self, callback) -> None:
        """Subscribe to notification events.
        
        Args:
            callback: Function to call when a notification is received
            
        Returns:
            None
            
        Raises:
            Various exceptions from subscribe
        """
        subscription = """
        subscription OnNotification {
            notification {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """
        
        self.client.subscribe(subscription, callback)


class AsyncNotificationResource:
    """Async Notification resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the Notification resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_notifications(self) -> List[Dict[str, Any]]:
        """Get all notifications.
        
        Returns:
            List of notifications
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNotifications {
            notifications {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "notifications" not in result:
            raise APIError("Invalid response format: missing notifications field")
        
        return result["notifications"]
    
    async def get_notification(self, id: str) -> Dict[str, Any]:
        """Get a notification by ID.
        
        Args:
            id: The notification ID
            
        Returns:
            The notification info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetNotification($id: String!) {
            notification(id: $id) {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "notification" not in result:
            raise APIError("Invalid response format: missing notification field")
        
        return result["notification"]
    
    async def mark_notification_read(self, id: str) -> Dict[str, Any]:
        """Mark a notification as read.
        
        Args:
            id: The notification ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MarkNotificationRead($id: String!) {
            markNotificationRead(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("markNotificationRead", {}).get("success", False):
            message = result.get("markNotificationRead", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mark notification as read: {message}")
        
        return result["markNotificationRead"]
    
    async def mark_all_notifications_read(self) -> Dict[str, Any]:
        """Mark all notifications as read.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation MarkAllNotificationsRead {
            markAllNotificationsRead {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("markAllNotificationsRead", {}).get("success", False):
            message = result.get("markAllNotificationsRead", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to mark all notifications as read: {message}")
        
        return result["markAllNotificationsRead"]
    
    async def dismiss_notification(self, id: str) -> Dict[str, Any]:
        """Dismiss a notification.
        
        Args:
            id: The notification ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DismissNotification($id: String!) {
            dismissNotification(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("dismissNotification", {}).get("success", False):
            message = result.get("dismissNotification", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to dismiss notification: {message}")
        
        return result["dismissNotification"]
    
    async def dismiss_all_notifications(self) -> Dict[str, Any]:
        """Dismiss all notifications.
        
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DismissAllNotifications {
            dismissAllNotifications {
                success
                message
            }
        }
        """
        
        result = await self.client.execute_query(mutation)
        
        if not result.get("dismissAllNotifications", {}).get("success", False):
            message = result.get("dismissAllNotifications", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to dismiss all notifications: {message}")
        
        return result["dismissAllNotifications"]
    
    async def subscribe_to_notifications(self, callback) -> None:
        """Subscribe to notification events.
        
        Args:
            callback: Async function to call when a notification is received
            
        Returns:
            None
            
        Raises:
            Various exceptions from subscribe
        """
        subscription = """
        subscription OnNotification {
            notification {
                id
                type
                importance
                subject
                description
                timestamp
                read
            }
        }
        """
        
        await self.client.subscribe(subscription, callback)
