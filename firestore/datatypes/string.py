from firestore.errors import ValidationError


class String(object):

    __slots__ = ("minimum", "maximum", "required", "pk", "unique", "default", "coerce", "_name", "value")
    
    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        self.required = kwargs.get("required")
        self.pk = kwargs.get("pk")
        self.unique = kwargs.get("unique")
        self.default = kwargs.get("default")
        self.coerce = kwargs.get("coerce", True)

    def __get__(self, instance, metadata):
        pass

    def __set__(self, instance, value):
        # first we run validation rules
        self.value = self.validate(value)
        instance._data.set(self._name, {
            "type": str,
            "value": self.value,
            "required": self.required
        })

    def __set_name__(self, instance, name):
        """This is called with the value of the object of
        reference's attribute passed in so we can get the name
        of the field attribute
        """
        self._name = name
    
    def validate(self, value):
        max_msg = f'{self._name} must have a maximum len of {self.maximum}, found {len(value)}'
        min_msg = f'{self._name} must have minimum len of {self.minimum}, found {len(value)}'

        if self.minimum and self.minimum > len(value):
            raise ValidationError(min_msg)
        if self.maximum and self.maximum < len(value):
            raise ValidationError(max_msg)
        if self.required and not value:
            raise ValidationError(f'{self._name} is a required field')
        if isinstance(value, str):
            return value
        if not isinstance(value, str) and self.coerce:
            if isinstance(value, int) or isinstance(value, float):
                return str(value)
            raise ValueError(f'Can not coerce {type(value)} to str')
        raise ValueError(f'{value} is not of type str and coerce is {self.coerce}')
