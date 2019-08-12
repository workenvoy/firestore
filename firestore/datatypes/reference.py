import importlib
from firestore.datatypes.base import Base


class Reference(Base):
    """Firestore referable elements i.e. Project ID,
    Document ID etc.
    """

    __slots__ = ("_name", "doc_ref")

    def __init__(self, *args, **kwargs):
        self.doc_ref = args[0]
        super(Reference, self).__init__(*args, **kwargs)

    def __set__(self, instance, value):
        self.validate(value, instance)
        instance.add_field(self, value)
        instance.__mutated__ = True

    def validate(self, value, instance):
        # The document class instruments and stores fields under
        # the field cache dict when it is initialized.
        # Because the document reference is the first argument
        # given to the Reference descriptor and saved in
        # the instance variable `doc_ref` we can assess
        # and retrieve this from the instance of this class
        # that lives in the field cache of the instance (Parent Document)
        # where this class was added to as a document field.
        DocRef = instance.fields_cache.get(self._name).doc_ref
        if isinstance(DocRef, str):
            DocRef = instance.__deref__(DocRef)
        if not isinstance(value, DocRef):
            clsname = type(instance).__name__
            raise AttributeError(f"{clsname} expected a `{DocRef}` not a {type(value)}")
