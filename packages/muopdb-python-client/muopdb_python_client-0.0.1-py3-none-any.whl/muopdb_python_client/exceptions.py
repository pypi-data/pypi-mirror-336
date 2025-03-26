"""
Custom exceptions for the MuopDB client.
"""

class MuopDBError(Exception):
    """Base exception for all MuopDB client errors."""
    pass

class MuopDBConnectionError(MuopDBError):
    """Raised when there are connection issues with the MuopDB server."""
    pass

class MuopDBAuthenticationError(MuopDBError):
    """Raised when authentication fails."""
    pass

class MuopDBValidationError(MuopDBError):
    """Raised when input validation fails."""
    pass

class MuopDBResponseError(MuopDBError):
    """Raised when the server returns an error response."""
    pass 