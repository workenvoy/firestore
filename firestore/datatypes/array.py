from .datatype import Datatype


class Array(Datatype):
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
    pass
