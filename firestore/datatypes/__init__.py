class Datatype(object):
    """
    Base datatype object to be used by all classes
    """

    pass


from .array import Array
from .boolean import Boolean
from .byte import Byte
from .datatype import Datatype
from .number import Float
from .geopoint import Geopoint
from .number import Integer
from .map import Map
from .null import Null
from .reference import Reference
from .string import String
from .timestamp import Timestamp


__all__ = [
    "Array",
    "Boolean",
    "Byte",
    "Datatype",
    "Float",
    "Geopoint",
    "Integer",
    "Map",
    "Null",
    "Reference",
    "String",
    "Timestamp"
]
