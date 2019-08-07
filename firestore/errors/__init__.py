__all__ = ("InvalidFieldError", "ValidationError")


class DuplicateError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


class InvalidFieldError(Exception):
    pass


class UnknownFieldError(Exception):
    pass


class ValidationError(Exception):
    pass
