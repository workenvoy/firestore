__all__ = ("InvalidFieldError", "ValidationError")


class InvalidDocumentError(Exception):
    pass


class InvalidFieldError(Exception):
    pass


class UnknownFieldError(Exception):
    pass


class ValidationError(Exception):
    pass
