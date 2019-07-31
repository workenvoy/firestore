from .datatype import Datatype


class Byte(Datatype):
    """
    Firestore cloud db byte datatype. Up to 1,048,487 bytes (1 MiB - 89 bytes).
    Only the first 1,500 bytes are considered by queries
    """
    pass
