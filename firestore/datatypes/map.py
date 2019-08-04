from .datatype import Datatype


class MapSchema(object):
    """
    A map schema defines a helper by which maps can be populated
    so there is no need to use default python dicts"""

    pass


class Map(object):
    """Maps as defined by firestore represent an object saved within a document.
    In python speak - A map is akin to a dictionary.

    Maps on Firestore cloud are an ordered collection of key value pairs
    and the firestore library mimics this sorting at retrieval and traversal
    which is sufficient for almost use cases encountered in the wild
    """

    def __init__(self, *args, **kwargs):
        pass
