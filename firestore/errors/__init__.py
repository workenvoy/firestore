__all__ = ("InvalidFieldError", "ValidationError")


class CollectionError(Exception):
    pass


class DuplicateError(Exception):
    pass


class InvalidDocumentError(Exception):
    pass


class InvalidFieldError(Exception):
    pass


class NotFoundError(Exception):
    pass


class OfflineDocumentError(Exception):
    pass


class PKError(Exception):
    pass


class UnknownFieldError(Exception):
    pass


class ValidationError(Exception):
    pass
