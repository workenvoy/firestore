"""
    firestore.containers.document
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    John Cleese (Commentator): Ah no, they're not. No they didn't realize
    they were supposed to start. Never mind, we'll soon sort that out, the
    judge is explaining it to them now. I think Nigel and Gervaise have
    got the idea. All set to go.

    :copyright: 2019 Workhamper
    :license: MIT
"""
from firestore.errors import InvalidDocumentError
# from firestore.datatypes.base import Base


class Cache(dict):
    """
    A class to make attribute lookup and writing
    swift and fast without the need for attribute access
    notation instead defaulting to object access notation
    """

    def __init__(self, *args, **kwargs):
        self._pk = False
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, key):
        # less error prone
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
    
    def add(self, key, value):
        self.__setattr__(key, value)


class Document(object):
    """Documents are recommended to be used when saving objects
    to firestore. They ensure a schema exists under which data can be
    stored i.e. reducing the error of typing name and naame across
    two different documents.

    They also help to group together commonly used actions across documents
    i.e. setting and saving, querying, and updating document instances.
    """

    @staticmethod
    def __deref__(instance, *args, **kwargs):
        """custom method to load document constraints"""

        # Document constraints are the constraints found on
        # fields that pertain to the entire document and not
        # just the field.
        # For instance required, unique, pk etc... These fields
        # do not have any meaning without the larger document, and or
        # Collection in the picture.
        pass

    def __init__(self, *args, **kwargs):
        """
        Root document holding all the utility methods
        needed for persistence to cloud firestore
        """
        self._data = Cache()
        self.fields_cache = {
            k: v for k,v in type(self).__dict__.items() if k not in ['__module__', '__doc__']
        }

    def add_field(self, field, value):
        """
        Add a field to this instance's data for persistence
        taking into cognizance all the validations present on the field
        """
        self._data.add(field._name, value)
    
    def get_field(self, field):
        """
        Get a field form the internal _data store of field values
        """
        return self._data.get(field._name)

    def save(self):
        """
        Save changes made to document to cloud firestore.
        """
        pass

    def persist(self):
        """Save changes made to this document and any children of this
        document to cloud firestore
        """
        pass

    def transaction(self):
        """
        Perform a transaction i.e. persist all changes or roll back
        entire transaction
        """
        pass
