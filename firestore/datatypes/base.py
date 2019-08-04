class Base(object):
    """
    Super class for document valid datatypes
    """

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.get("pk")
        self.required = kwargs.get("required")
        self.default = kwargs.get("default")
        self.unique = kwargs.get("unique")

    def __get__(self, instance, metadata):
        return instance.get_field(self)

    def __set__(self, instance, value):
        self.validate(value)
        instance.add_field(self, value)

    def __set_name__(self, cls, name):
        self._name = name

    def validate(self, value):
        pass