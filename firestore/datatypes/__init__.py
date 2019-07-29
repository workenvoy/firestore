class Datatype(object):
    """
    Base datatype object to be used by all classes
    """

    pass


# from .boolean import Boolean
# from .byte import Byte
# from .datetime import Datetime
# from .float import Float
# from .geopoint import Geopoint
# from .integer import Integer
# from .map import Map
# from .null import Null
from .reference import Reference
# from .string import String


__all__ = [
    "Array",
    "Boolean",
    "Byte",
    "Datatype",
    "Datetime",
    "Float",
    "Geopoint",
    "Integer",
    "Map",
    "Null",
    "Reference",
    "String",
]
