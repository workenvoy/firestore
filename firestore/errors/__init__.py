__all__ = ("InvalidFieldError", "ValidationError")


class InvalidFieldError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


class ValidationError(Exception):
    pass
