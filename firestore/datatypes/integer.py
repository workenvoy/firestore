from firestore.datatypes.number import Number


class Integer(Number):
    """
    64bit signed non decimal integer
    """

    def __init__(self, *args, **kwargs):
        self.py_type = int
        super(Integer, self).__init__(*args, **kwargs)
