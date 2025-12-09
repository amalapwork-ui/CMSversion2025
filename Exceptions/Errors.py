class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class NotFoundError(Exception):
    """Raised when a requested record is not found."""
    pass

class DBError(Exception):
    """Wraps low-level database errors."""
    pass

class ConflictError(Exception):
    """Raised when a business rule conflict occurs (slot clashes, etc)."""
    pass

class PermissionError(Exception):
    """Raised when a user tries to access something they shouldn't."""
    pass
class AppError(Exception):
    """Base class for all application-specific errors."""
    pass