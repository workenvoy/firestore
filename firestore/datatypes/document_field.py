from abc import ABCMeta


class DocumentField(metaclass=ABCMeta):
    """This is the base class for all fields

    All fields inherit from DocumentField
    to house implementation of share functionality expected
    from all field instances

    >>> documentField = DocumentField()
    """

    pass
