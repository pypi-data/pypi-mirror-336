"""Authentication module for unraid_api."""
import time
import json
import logging
import os
from typing import Dict, Optional, Tuple, Union, Any

import httpx

from .exceptions import AuthenticationError, TokenExpiredError, ConnectionError

logger = logging.getLogger(__name__)


class AuthManager:
    """Handles authentication and token management for Unraid GraphQL API."""

    def __init__(
        self,
        host: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
        verify_ssl: bool = False,
    ):
        """Initialize the authentication manager.
        
        Args:
            host: The hostname or IP address of the Unraid server
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            token_persistence_path: Path to save tokens for persistence (default: None)
            verify_ssl: Whether to verify SSL certificates (default: False)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.token_persistence_path = token_persistence_path
        self.verify_ssl = verify_ssl
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expiry: Optional[int] = None
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"
        
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
    
    def _save_tokens(self) -> None:
        """Save tokens to the persistence path if configured."""
        if not self.token_persistence_path:
            return
        
        token_data = {
            "access_token": self._access_token,
            "refresh_token": self._refresh_token,
            "expiry": self._token_expiry
        }
        
        try:
            os.makedirs(os.path.dirname(self.token_persistence_path), exist_ok=True)
            with open(self.token_persistence_path, "w") as f:
                json.dump(token_data, f)
        except Exception as e:
            logger.warning(f"Failed to persist tokens: {e}")
    
    def login(self, username: str, password: str) -> str:
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
            response = httpx.post(
                self._base_url,
                json={"query": mutation, "variables": variables},
                timeout=10.0,
                verify=self.verify_ssl
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
            self._save_tokens()
            
            return self._access_token
            
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(f"HTTP error during login: {e}")
    
    def connect_sign_in(self, connect_token: str) -> str:
        """Sign in using Unraid Connect token.
        
        Args:
            connect_token: The Unraid Connect token
            
        Returns:
            The access token
            
        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If the server cannot be reached
        """
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
            response = httpx.post(
                self._base_url,
                json={"query": mutation, "variables": variables},
                timeout=10.0,
                verify=self.verify_ssl
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
            self._save_tokens()
            
            return self._access_token
            
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(f"HTTP error during connect sign-in: {e}")
    
    def refresh_token(self) -> str:
        """Refresh the access token using the refresh token.
        
        Returns:
            The new access token
            
        Raises:
            TokenExpiredError: If the refresh token is expired or invalid
            ConnectionError: If the server cannot be reached
        """
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
            response = httpx.post(
                self._base_url,
                json={"query": mutation, "variables": variables},
                timeout=10.0,
                verify=self.verify_ssl
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
            self._save_tokens()
            
            return self._access_token
            
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise TokenExpiredError("Refresh token has expired")
            raise ConnectionError(f"HTTP error during token refresh: {e}")
    
    def get_access_token(self) -> str:
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
            return self.refresh_token()
        
        return self._access_token
    
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated with a valid token.
        
        Returns:
            True if authenticated, False otherwise
        """
        if not self._access_token or not self._token_expiry:
            return False
        
        return self._token_expiry > time.time()
    
    def logout(self) -> None:
        """Clear authentication tokens."""
        self._access_token = None
        self._refresh_token = None
        self._token_expiry = None
        
        # Remove persisted tokens
        if self.token_persistence_path:
            try:
                os.remove(self.token_persistence_path)
            except Exception as e:
                logger.warning(f"Failed to clear persisted tokens: {e}")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get the authorization headers for API requests.
        
        Returns:
            Dict with authorization headers
            
        Raises:
            AuthenticationError: If not authenticated
        """
        token = self.get_access_token()
        return {"Authorization": f"Bearer {token}"}
