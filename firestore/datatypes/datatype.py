from firestore.datatypes.base import Base
from firestore.datatypes import (
    Array,
    Boolean,
    Byte,
    Float,
    Geopoint,
    Map,
    Null,
    Integer,
    Float,
    Reference,
    String,
)


class Datatype(object):
    """
    Lazy class for the firestore library
    """

    def __new__(cls, *args, **kwargs):
        target = args[0]
        target = datatypes.get(args[0].lower())

        # remove the datatypes designation string because
        # specific types i.e. Integer, String, Map don't need it
        # and don't support or expect it
        args = args[1:]
        return target(*args, **kwargs)


datatypes = {
    "array": Array,
    "boolean": Boolean,
    "byte": Byte,
    "float": Float,
    "geopoint": Geopoint,
    "integer": Integer,
    "map": Map,
    "null": Null,
    "reference": Reference,
    "string": String,
}
