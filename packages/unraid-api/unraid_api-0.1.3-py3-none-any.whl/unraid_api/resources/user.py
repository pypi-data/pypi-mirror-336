"""User resource for unraid_api."""
import logging
from typing import Any, Dict, List, Optional, Union

from ..exceptions import APIError, GraphQLError, OperationError

logger = logging.getLogger(__name__)


class UserResource:
    """User resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the User resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users.
        
        Returns:
            List of users
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetUsers {
            users {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "users" not in result:
            raise APIError("Invalid response format: missing users field")
        
        return result["users"]
    
    def get_user(self, id: str) -> Dict[str, Any]:
        """Get a user by ID.
        
        Args:
            id: The user ID
            
        Returns:
            The user info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetUser($id: String!) {
            user(id: $id) {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(query, variables)
        
        if "user" not in result:
            raise APIError("Invalid response format: missing user field")
        
        return result["user"]
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get the current authenticated user.
        
        Returns:
            The current user info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetCurrentUser {
            currentUser {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        result = self.client.execute_query(query)
        
        if "currentUser" not in result:
            raise APIError("Invalid response format: missing currentUser field")
        
        return result["currentUser"]
    
    def create_user(self, username: str, password: str, name: Optional[str] = None, 
                   description: Optional[str] = None, email: Optional[str] = None, 
                   roles: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a new user.
        
        Args:
            username: The username
            password: The password
            name: The display name (optional)
            description: The description (optional)
            email: The email address (optional)
            roles: The list of roles (optional)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """
        
        variables = {
            "input": {
                "username": username,
                "password": password
            }
        }
        
        if name is not None:
            variables["input"]["name"] = name
        
        if description is not None:
            variables["input"]["description"] = description
        
        if email is not None:
            variables["input"]["email"] = email
        
        if roles is not None:
            variables["input"]["roles"] = roles
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("createUser", {}).get("success", False):
            message = result.get("createUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create user: {message}")
        
        return result["createUser"]
    
    def update_user(self, id: str, username: Optional[str] = None, 
                   name: Optional[str] = None, description: Optional[str] = None,
                   email: Optional[str] = None, roles: Optional[List[str]] = None) -> Dict[str, Any]:
        """Update a user.
        
        Args:
            id: The user ID
            username: The new username (optional)
            name: The new display name (optional)
            description: The new description (optional)
            email: The new email address (optional)
            roles: The new list of roles (optional)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateUser($id: String!, $input: UpdateUserInput!) {
            updateUser(id: $id, input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """
        
        variables = {
            "id": id,
            "input": {}
        }
        
        if username is not None:
            variables["input"]["username"] = username
        
        if name is not None:
            variables["input"]["name"] = name
        
        if description is not None:
            variables["input"]["description"] = description
        
        if email is not None:
            variables["input"]["email"] = email
        
        if roles is not None:
            variables["input"]["roles"] = roles
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("updateUser", {}).get("success", False):
            message = result.get("updateUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update user: {message}")
        
        return result["updateUser"]
    
    def change_user_password(self, id: str, password: str) -> Dict[str, Any]:
        """Change a user's password.
        
        Args:
            id: The user ID
            password: The new password
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ChangeUserPassword($id: String!, $password: String!) {
            changeUserPassword(id: $id, password: $password) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id,
            "password": password
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("changeUserPassword", {}).get("success", False):
            message = result.get("changeUserPassword", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to change user password: {message}")
        
        return result["changeUserPassword"]
    
    def delete_user(self, id: str) -> Dict[str, Any]:
        """Delete a user.
        
        Args:
            id: The user ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteUser($id: String!) {
            deleteUser(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = self.client.execute_query(mutation, variables)
        
        if not result.get("deleteUser", {}).get("success", False):
            message = result.get("deleteUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete user: {message}")
        
        return result["deleteUser"]


class AsyncUserResource:
    """Async User resource for the Unraid GraphQL API."""
    
    def __init__(self, client):
        """Initialize the User resource.
        
        Args:
            client: The Unraid client
        """
        self.client = client
    
    async def get_users(self) -> List[Dict[str, Any]]:
        """Get all users.
        
        Returns:
            List of users
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetUsers {
            users {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "users" not in result:
            raise APIError("Invalid response format: missing users field")
        
        return result["users"]
    
    async def get_user(self, id: str) -> Dict[str, Any]:
        """Get a user by ID.
        
        Args:
            id: The user ID
            
        Returns:
            The user info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetUser($id: String!) {
            user(id: $id) {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(query, variables)
        
        if "user" not in result:
            raise APIError("Invalid response format: missing user field")
        
        return result["user"]
    
    async def get_current_user(self) -> Dict[str, Any]:
        """Get the current authenticated user.
        
        Returns:
            The current user info
            
        Raises:
            Various exceptions from execute_query
        """
        query = """
        query GetCurrentUser {
            currentUser {
                id
                username
                name
                description
                roles
                lastLogin
                email
            }
        }
        """
        
        result = await self.client.execute_query(query)
        
        if "currentUser" not in result:
            raise APIError("Invalid response format: missing currentUser field")
        
        return result["currentUser"]
    
    async def create_user(self, username: str, password: str, name: Optional[str] = None, 
                        description: Optional[str] = None, email: Optional[str] = None, 
                        roles: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a new user.
        
        Args:
            username: The username
            password: The password
            name: The display name (optional)
            description: The description (optional)
            email: The email address (optional)
            roles: The list of roles (optional)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """
        
        variables = {
            "input": {
                "username": username,
                "password": password
            }
        }
        
        if name is not None:
            variables["input"]["name"] = name
        
        if description is not None:
            variables["input"]["description"] = description
        
        if email is not None:
            variables["input"]["email"] = email
        
        if roles is not None:
            variables["input"]["roles"] = roles
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("createUser", {}).get("success", False):
            message = result.get("createUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to create user: {message}")
        
        return result["createUser"]
    
    async def update_user(self, id: str, username: Optional[str] = None, 
                        name: Optional[str] = None, description: Optional[str] = None,
                        email: Optional[str] = None, roles: Optional[List[str]] = None) -> Dict[str, Any]:
        """Update a user.
        
        Args:
            id: The user ID
            username: The new username (optional)
            name: The new display name (optional)
            description: The new description (optional)
            email: The new email address (optional)
            roles: The new list of roles (optional)
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation UpdateUser($id: String!, $input: UpdateUserInput!) {
            updateUser(id: $id, input: $input) {
                success
                message
                user {
                    id
                    username
                    name
                    description
                    roles
                    email
                }
            }
        }
        """
        
        variables = {
            "id": id,
            "input": {}
        }
        
        if username is not None:
            variables["input"]["username"] = username
        
        if name is not None:
            variables["input"]["name"] = name
        
        if description is not None:
            variables["input"]["description"] = description
        
        if email is not None:
            variables["input"]["email"] = email
        
        if roles is not None:
            variables["input"]["roles"] = roles
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("updateUser", {}).get("success", False):
            message = result.get("updateUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to update user: {message}")
        
        return result["updateUser"]
    
    async def change_user_password(self, id: str, password: str) -> Dict[str, Any]:
        """Change a user's password.
        
        Args:
            id: The user ID
            password: The new password
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation ChangeUserPassword($id: String!, $password: String!) {
            changeUserPassword(id: $id, password: $password) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id,
            "password": password
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("changeUserPassword", {}).get("success", False):
            message = result.get("changeUserPassword", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to change user password: {message}")
        
        return result["changeUserPassword"]
    
    async def delete_user(self, id: str) -> Dict[str, Any]:
        """Delete a user.
        
        Args:
            id: The user ID
            
        Returns:
            The mutation response
            
        Raises:
            Various exceptions from execute_query
        """
        mutation = """
        mutation DeleteUser($id: String!) {
            deleteUser(id: $id) {
                success
                message
            }
        }
        """
        
        variables = {
            "id": id
        }
        
        result = await self.client.execute_query(mutation, variables)
        
        if not result.get("deleteUser", {}).get("success", False):
            message = result.get("deleteUser", {}).get("message", "Unknown error")
            raise OperationError(f"Failed to delete user: {message}")
        
        return result["deleteUser"]
