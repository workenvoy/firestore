from firestore.errors import ValidationError
from firestore.datatypes.base import Base


class Boolean(Base):
    """
    Represents a boolean field in the firestore Document instance

    .. py:function:: enumerate(sequence[, start=0])

        Return an iterator that yields tubles of an index and an item of the
        *sequence*. (And so on.)
    """

    __slots__ = ("value", "coerce", "_name")

    def __init__(self, *args, **kwargs):
        self.coerce = kwargs.get("coerce", True)
        super(Boolean, self).__init__(*args, **kwargs)

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
