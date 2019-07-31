from .datatype import Datatype



class String(Datatype):
    """
    UTF-8 Text strings

    Up to 1,048,487 bytes (1 MiB - 89 bytes). Only the first 1,500 bytes
    of the UTF-8 representation are considered by queries
    """
    def __init__(self, **kwargs):
        self.options = kwargs.get('options')

    def validate(self, value):
        if(self.options) and value not in self.options:
            raise AttributeError(f"String values must be one of {self.options}")
