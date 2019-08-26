from firestore.errors import PKError


PKS = (
    "integer",
    "float",
    "string",
    "geopoint"  # For the weird guys at G
)

class Base(object):
    """
    Super class for document valid datatypes
    """

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.get("pk")
        self.required = kwargs.get("required")
        self.default = kwargs.get("default")
        self.unique = kwargs.get("unique")
        self.textsearch = kwargs.get("textsearch")
        self.options = kwargs.get("options")
        self.value = None

    def __get__(self, instance, metadata):
        return instance.get_field(self)

    def __set__(self, instance, value):
        if self.pk:
            if type(self).__name__.lower() not in PKS:
                raise PKError(f'Fields of type {type(self).__name__} can not be set as primary key')
            instance.pk = self

        if self.unique:
            instance.uniques = self._name, value
        self.validate(value, instance)
        self.value = value
        instance.__mutated__ = True
        instance.add_field(self, value)

    def __set_name__(self, cls, name):
        self._name = name

    def cast(self, instance, value):
        self.validate(value, instance)
        if isinstance(value, self.py_type):  # pylint: disable=no-member
            return value
        return self.py_type(value)  # pylint: disable=no-member

    def validate(self, value, instance=None):
        pass
