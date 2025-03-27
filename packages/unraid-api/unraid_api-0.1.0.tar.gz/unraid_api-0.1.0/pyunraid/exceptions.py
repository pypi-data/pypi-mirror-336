"""Exceptions for the pyunraid library."""

class PyUnraidError(Exception):
    """Base exception for pyunraid errors."""
    pass


class AuthenticationError(PyUnraidError):
    """Raised when authentication fails."""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when the authentication token has expired."""
    pass


class ConnectionError(PyUnraidError):
    """Raised when a connection to the Unraid server fails."""
    pass


class APIError(PyUnraidError):
    """Raised when the Unraid API returns an error."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class ValidationError(PyUnraidError):
    """Raised when input validation fails."""
    pass


class ResourceNotFoundError(PyUnraidError):
    """Raised when a requested resource is not found."""
    pass


class OperationError(PyUnraidError):
    """Raised when an operation fails."""
    pass


class GraphQLError(PyUnraidError):
    """Raised when a GraphQL error occurs."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class SubscriptionError(PyUnraidError):
    """Raised when a subscription operation fails."""
    pass


class RateLimitError(PyUnraidError):
    """Raised when rate limits are exceeded."""
    pass
