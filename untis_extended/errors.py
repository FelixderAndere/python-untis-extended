""" Exceptions """

class UntisError(Exception):
    """Base class for all Untis-related errors."""
    pass

# Network / Connection

class UntisConnectionError(UntisError):
    """Raised when a connection to the Untis API fails."""
    pass

class UntisTimeoutError(UntisError):
    """Raised when a request to the Untis API times out."""
    pass


# Authentication

class UntisCredentialsError(UntisError):
    """Raised when login credentials are invalid or authentication fails."""
    pass

class UntisAuthError(UntisError):
    """Raised when an authentication token is invalid or expired."""
    pass


# API / Data handling

class UntisAPIError(UntisError):
    """
    Raised when the Untis API returns an unexpected or invalid response.
    Covers general API-level issues that are not purely data parsing errors.
    """
    pass


class UntisDataError(UntisError):
    """
    Raised when received data cannot be processed, is incomplete,
    or does not match the expected structure/schema.
    """
    pass