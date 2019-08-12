from firestore.containers.collection import Collection
from firestore.datatypes.base import Base

from firestore.errors import ValidationError


class MapSchema(Collection):
    """
    A map schema defines a helper by which maps can be populated
    so there is no need to use default python dicts"""

    def __init__(self, *args, **kwargs):
        super(MapSchema, self).__init__(*args, **kwargs)


class Map(Base):
    """Maps as defined by firestore represent an object saved within a document.
    In python speak - A map is akin to a dictionary.

    Maps on Firestore cloud are an ordered collection of key value pairs
    and the firestore library mimics this sorting at retrieval and traversal
    which is sufficient for almost use cases encountered in the wild
    """

    def __init__(self, *args, **kwargs):
        try:
            self.map_ref = args[0]
        except IndexError:
            self.map_ref = None
        super(Map, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        self.validate(value)

        # if a mapschema was passed in to the document
        # field map descriptor field then it is expected
        # that a mapping or dict will be the input value.
        # If the input is a dict then convert it to a map schema
        # and save otherwise save the map schema.
        # If no mapschema was used then save the dict as is.
        if self.map_ref:
            value = self.map_ref(**value) if isinstance(value, dict) else value
        self.value = value
        instance.add_field(self, value)
        instance.__mutated__ = True

    def validate(self, value):
        # If the map descriptor field has any
        # children at all then it should be
        # a MapSchema instance of keys and values
        # expected in the map.
        # Maps unfortunately can not be marked as pk, as
        # a required field, or as having a default value.
        # You can however map the keys in the
        # map schema instance as required.
        if self.map_ref:
            if not isinstance(value, (MapSchema, dict)):
                raise ValueError()
            if isinstance(value, dict):
                _schema = self.map_ref.__autospector__()

                for k in _schema:
                    # get a local copy of the field instance
                    f = _schema.get(k)
                    v = value.get(k)
                    f.validate(v)
            else:
                # If mapschema then validation happens at map schema level
                value._presave()
