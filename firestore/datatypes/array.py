from firestore.datatypes.base import Base

from firestore.errors import ValidationError
from firestore.datatypes._special_array import SpecialArray


class Array(Base):
    """
    An array is a sequence datatype and can not contain another array
    as one of its elements.

    Within an array, elements maintain the position assigned to them. When
    sorting two or more arrays, arrays are ordered based on their elements
    values.

    When comparing arrays, the first elements of each array is compared. If the
    first elements are equal, then the next elements are compared - and so on until
    a difference is found. If an array runs out of elements to compare but is equal
    up to that point, then the shorter array is ordered before the longer array.

    For example [1, 2, 3] < [1, 2, 3, 1] < [2]. The array [2] has the greatest first
    element value. The array [1, 2, 3] has elements equal to the first three elements
    of [1, 2, 3, 1] but is shorter in length.
    """

    __slots__ = ("minimum", "maximum", "value", "py_type", "sa")

    def __init__(self, *args, **kwargs):

        # Special array is an overriden python list created to provide
        # special deref and ref parsing capabilities on Arrays of
        # specific Firestore Field class types
        self.sa = SpecialArray()
        try:
            # If an array field type contains an arg child then it is
            # safe to assume it is a field class type i.e. Reference, String 
            array_data_type = args[0]
        except:
            pass
        else:
            # Log the field type locally as an expected type for the Array
            self.sa.expected = array_data_type

        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        self.py_type = SpecialArray
        super(Array, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        self.validate(value)
        if self.sa.expected:
            # Whatever field type is passed in as expected, use its own
            # cast method to validate and cast it before storing
            # in the parent instance document
            value = [self.sa.expected.cast(instance, item) for item in value]
        self.value = value
        instance.__mutated__ = True
        instance.add_field(self, value)

    def validate(self, value, instance=None):
        """Validate the value conforms to the dataype expected of Arrays"""
        if not isinstance(value, (list, tuple)):
            raise ValidationError(f'Arrays can only be assigned iterables like lists - found {value}')
        if self.minimum and self.minimum > len(value):
            raise ValidationError(
                f"Array {self._name} must me a minimum of len {self.minimum}"
            )
        if self.maximum and self.maximum < len(value):
            raise ValidationError(
                f"Array {self._name} must be a maximum of len {self.maximum}"
            )
