"""PyUnraid: Python Library for Unraid GraphQL API."""

from .client import UnraidClient
from .client_async import AsyncUnraidClient
from .exceptions import (
    PyUnraidError,
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

__version__ = "0.1.0"
__all__ = [
    "UnraidClient",
    "AsyncUnraidClient",
    "PyUnraidError",
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
