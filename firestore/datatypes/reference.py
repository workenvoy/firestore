import importlib
from firestore import Document
from firestore.datatypes.base import Base
from firestore.db.connection import ResultSet


#TODO: Dereference strings into document instances using __collection__ lookup on access 
# and convert into Firestore refs on write using same tactic but throwing an error when 
# a document with that ID is not found


class Reference(Base):
    """Firestore referable elements i.e. Project ID,
    Document ID etc.
    """

    __slots__ = ("_name", "doc_ref")

    def __init__(self, *args, **kwargs):
        self.doc_ref = args[0]
        if not isinstance(args[0], Document):
            raise ValueError(f"Reference must be a {Document}")
        super(Reference, self).__init__(*args, **kwargs)
    
    def __get__(self, instance, metadata):
        ref_field = instance.fields_cache.get(self._name)
        return ref_field


    def __set__(self, instance, value):
        self.validate(value, instance)
        self.value = value
        instance.add_field(self, value)
        instance.__mutated__ = True

        # when a string is used check to ensure the string matches the
        # string representation of the descriptor field
        # then load the document ref using that string
        # and throw an error if the document does not exist on cloud firestore

        # if a document type is used then check that the document type is of type
        # defined in reference descriptor object
        # Then check for __loaded__ or load the document from
        # cloud firestore and throw error if it
        # does not exist

    def validate(self, value, instance):
        # The document class instruments and stores fields under
        # the field cache dict when it is initialized.
        # Because the document reference is the first argument
        # given to the Reference descriptor and saved in
        # the instance variable `doc_ref` we can assess
        # and retrieve this from the instance of this class
        # that lives in the field cache of the instance (Parent Document)
        # where this class was added to as a document field.
        if isinstance(value, str):
            doc = self.doc_ref.get(value)
        if isinstance(value, (self.doc_ref, str)):
            return
        else:
            clsname = type(instance).__name__
            raise AttributeError(f"{clsname} expected a `{self.doc_ref}` not a {type(value)}")
