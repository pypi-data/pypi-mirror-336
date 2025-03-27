"""
KDAI Node Client - Exceptions

Custom exceptions for the KDAI Node Client.
"""


class KDAIException(Exception):
    """Base exception for all KDAI-related errors."""
    pass


class AuthenticationError(KDAIException):
    """Raised when node authentication fails."""
    pass


class ConnectionError(KDAIException):
    """Raised when connection to the KDAI server fails."""
    pass


class NodeAlreadyRunningError(KDAIException):
    """Raised when attempting to start a node that is already running."""
    pass


class RequestError(KDAIException):
    """Raised when an API request to the KDAI server fails."""
    pass


class TaskExecutionError(KDAIException):
    """Raised when a task execution fails."""
    pass


class ModelLoadError(KDAIException):
    """Raised when loading an AI model fails."""
    pass


class InsufficientResourcesError(KDAIException):
    """Raised when the node has insufficient resources for a task."""
    pass