class DomainError(Exception):
    """Base class for domain-level errors (invalid invariants, validation)."""


class InvalidEntityError(DomainError):
    """Raised when a domain invariant is violated or input is invalid.

    This should map to HTTP 422 Unprocessable Entity at the API layer.
    """


class NotFoundError(Exception):
    """Raised when an entity is not found (application-level error).

    This should map to HTTP 404 Not Found at the API layer.
    """


class ApplicationError(Exception):
    """Generic application-level errors that aren't domain validation.

    Use for transient or processing errors that should map to 422/500
    depending on context. Keep minimal for now.
    """
