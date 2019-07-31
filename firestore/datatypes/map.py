from .datatype import Datatype


class Map(Datatype):
    """Maps as defined by firestore represent an object saved within a document.
    In python speak - A map is akin to a dictionary.

    Maps on Firestore cloud are an ordered collection of key value pairs
    and the firestore library mimics this sorting at retrieval and traversal
    which is sufficient for almost use cases encountered in the wild
    """
    pass
