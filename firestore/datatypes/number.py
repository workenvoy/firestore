from .datatype import Datatype


class Integer(Datatype):
    """
    64bit signed non decimal integer
    """
    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)


class Float(Datatype):
    """
    64bit double precision IEEE 754
    """
    def __init__(self, *args, **kwargs):
        super(Float, self).__init__(*args, **kwargs)
