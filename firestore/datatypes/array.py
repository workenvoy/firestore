from firestore.datatypes.base import Base

from firestore.errors import ValidationError


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

    __slots__ = ("minimum", "maximum", "value")

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        super(Array, self).__init__(*args, **kwargs)

    def validate(self, value):
        """Validate the value conforms to the dataype expected of Arrays"""
        if self.minimum and self.minimum > len(value):
            raise ValidationError(
                f"Array {self._name} must me a minimum of len {self.minimum}"
            )
        if self.maximum and self.maximum < len(value):
            raise ValidationError(
                f"Array {self._name} must be a maximum of len {self.maximum}"
            )
