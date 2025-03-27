class FinaticError(Exception):
    """Base exception for all Finatic errors."""
    pass

class FinaticApiError(FinaticError):
    """Raised when the API returns an error."""
    pass

class FinaticAuthError(FinaticError):
    """Raised when there's an authentication error."""
    pass

class FinaticRateLimitError(FinaticError):
    """Raised when rate limit is exceeded."""
    pass

class FinaticValidationError(FinaticError):
    """Raised when there's a validation error."""
    pass

class FinaticNetworkError(FinaticError):
    """Raised when there's a network error."""
    pass 