
__all__ = (
    "InvalidFieldError"
)


class InvalidFieldError(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidFieldError, self).__init__(*args, **kwargs)
        try:
            msg = args[0]
        except IndexError:
            msg = "Document has an invalid field {}"
        self.message = kwargs.get("message") or msg
