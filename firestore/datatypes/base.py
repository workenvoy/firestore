


class Base(object):
    """
    Super class for document valid datatypes
    """

    def __init__(self, key, value, **kwargs):
        self.pk = kwargs.get('pk')
        self.required = kwargs.get('required')
        self.default = kwargs.get('default')
        self.unique = kwargs.get('unique')

    def __get__(self, instance, metadata):
        instance._data.get(self._name)

    def __set__(self, instance, value):
        self.validate(value)
        instance.add_field(self, value)

    def __set_name__(self, instance, name):
        self._name = name
    
    def validate(self, value):
        pass
