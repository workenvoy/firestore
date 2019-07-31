from .datatype import Datatype


class Null(Datatype):
    """
    Null mapping to python None globally unique object
    """
    def __init__(self, *args, **kwargs):
        pass
    
    def __eq__(self, comparable):
        return NotImplemented
