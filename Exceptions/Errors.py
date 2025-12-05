# Exceptions/Errors.py
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
    """Raised when a business rule conflict occurs (e.g., slot already taken)."""
    pass
