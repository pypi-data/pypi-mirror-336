"""Unraid API: Python Library for Unraid GraphQL API."""

from .client import UnraidClient
from .client_async import AsyncUnraidClient
from .exceptions import (
    UnraidAPIError,
    AuthenticationError,
    TokenExpiredError,
    ConnectionError,
    APIError,
    ValidationError,
    ResourceNotFoundError,
    OperationError,
    GraphQLError,
    SubscriptionError,
    RateLimitError,
)

__version__ = "0.1.3"
__all__ = [
    "UnraidClient",
    "AsyncUnraidClient",
    "UnraidAPIError",
    "AuthenticationError",
    "TokenExpiredError",
    "ConnectionError",
    "APIError",
    "ValidationError",
    "ResourceNotFoundError",
    "OperationError",
    "GraphQLError",
    "SubscriptionError",
    "RateLimitError",
]
