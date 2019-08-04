from firestore.errors import ValidationError


class Boolean(object):
    """
    Represents a boolean field in the firestore Document instance

    .. py:function:: enumerate(sequence[, start=0])

        Return an iterator that yields tubles of an index and an item of the
        *sequence*. (And so on.)
    """

    __slots__ = ("required", "default", "value", "coerce", "_name")

    def __init__(self, *args, **kwargs):
        self.required = kwargs.get("required")
        self.coerce = kwargs.get("coerce", True)

    def __get__(self, instance, metadata):
        pass

    def __set__(self, instance, value):
        self.value = self.validate(value)
        instance._data.add(self._name, self.value, self.required)

    def __set_name__(self, instance, name):
        self._name = name

    def validate(self, value):
        if self.coerce:
            return bool(value)
        if not isinstance(value, bool):
            raise ValidationError(
                f"Can not assign non-boolean to {self._name} type boolean"
            )
        return value
