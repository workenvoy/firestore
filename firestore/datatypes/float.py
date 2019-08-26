from firestore.datatypes.number import Number


class Float(Number):
    """
    64bit double precision IEEE 754
    """

    def __init__(self, *args, **kwargs):
        self.py_type = float
        super(Float, self).__init__(*args, **kwargs)
