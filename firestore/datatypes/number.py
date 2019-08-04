from firestore.errors import ValidationError
from firestore.datatypes.base import Base


class Number(Base):
    """
    Parent of numeric firestore types for method reuse only
    """

    __slots__ = ("minimum", "maximum", "required", "value", "pk", "_name", "coerce")

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        self.required = kwargs.get("required")
        self.pk = kwargs.get("pk")
        self.coerce = kwargs.get("coerce", False)
        super(Number, self).__init__(self, *args, **kwargs)

    def validate(self, value):
        """
        Run validation of numeric constraints
        """
        # Ensure only numeric values i.e. float and int are allowed to be assigned
        # as values.
        # Coercion is false by default as to not allow loss of precision unkowingly
        # or silently. To coerce int to float and float to int you the coerce
        # attribute of document fields must be explicitly set to true
        if not isinstance(value, (int, float)):
            raise ValueError(f"Non numeric type detected for field {self._name}")

        # Here an inspection of the class is necessary to allow for recognition
        # of the field type and allow the conversion from one numeric type
        # to another numeric type i.e. int -> float -> int as appropriate
        if self.__class__.__name__ is "Integer":
            if isinstance(value, float) and self.coerce:
                return int(value)
            if isinstance(value, float):
                raise ValueError(
                    f"Coercing float {self._name} to int might cause precision, explicitly set coerce to true"
                )

        # Unlike float -> int where precision loss is possible, converting an
        # integer value to float does mot raise a value error
        if self.__class__.__name__ is "Float" and isinstance(value, int):
            return float(value)

        # Apply minimum and maximum equality checks only after ensuring
        # that the correct datatypes were passed in taking the possibility
        # of absent minimum and maximum validataion parameter from the
        # numeric document field definition
        if self.minimum and value < self.minimum:
            raise ValidationError(
                f"{self._name} has value lower than minimum constraint"
            )
        if self.maximum and value > self.maximum:
            raise ValidationError(
                f"{self._name} has value higher than maximum constraint"
            )
        return value


class Integer(Number):
    """
    64bit signed non decimal integer
    """

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)


class Float(Number):
    """
    64bit double precision IEEE 754
    """

    def __init__(self, *args, **kwargs):
        super(Float, self).__init__(*args, **kwargs)
