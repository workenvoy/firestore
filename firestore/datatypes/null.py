from firestore.datatypes.base import Base


class Null(Base):
    """
    Null mapping to python None globally unique object
    """

    def __init__(self, *args, **kwargs):
        pass

    def __eq__(self, comparable):
        return NotImplemented
