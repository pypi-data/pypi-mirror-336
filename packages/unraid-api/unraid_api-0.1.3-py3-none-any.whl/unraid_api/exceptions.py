"""Exceptions for the unraid_api library."""

class UnraidAPIError(Exception):
    """Base exception for unraid_api errors."""
    pass


class AuthenticationError(UnraidAPIError):
    """Raised when authentication fails."""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when the authentication token has expired."""
    pass


class ConnectionError(UnraidAPIError):
    """Raised when a connection to the Unraid server fails."""
    pass


class APIError(UnraidAPIError):
    """Raised when the Unraid API returns an error."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class ValidationError(UnraidAPIError):
    """Raised when input validation fails."""
    pass


class ResourceNotFoundError(UnraidAPIError):
    """Raised when a requested resource is not found."""
    pass


class OperationError(UnraidAPIError):
    """Raised when an operation fails."""
    pass


class GraphQLError(UnraidAPIError):
    """Raised when a GraphQL error occurs."""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


class SubscriptionError(UnraidAPIError):
    """Raised when a subscription operation fails."""
    pass


class RateLimitError(UnraidAPIError):
    """Raised when rate limits are exceeded."""
    pass
