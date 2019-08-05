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
from firestore.errors import InvalidDocumentError, UnknownFieldError, ValidationError

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

    @classmethod
    def __autospector__(cls, *args, **kwargs):
        return {
            k: v for k, v in cls.__dict__.items() if k not in ["__module__", "__doc__"]
        }

    def __deref__(self, doc_ref):
        """
        Deref string based document references into classes
        upon instance assignment by looking up the doc_ref
        first in the globals of this module then walking
        up the directory tree until an instance is found
        or an error is thrown
        """
        raise NotImplementedError(
            "String dereferencing priority is low for now, will come back to this in a few weeks"
        )

    def __init__(self, *args, **kwargs):
        """
        Root document holding all the utility methods
        needed for persistence to cloud firestore
        """

        # This is the internal cache that holds all the field
        # values to be saved on google cloud firestore
        self._data = Cache()

        # Similar to the ._data instance cache. However this
        # is a collection of all descriptor instances
        # that exist on this document class.
        # Useful for pk, unique, required and other document
        # level validation.
        self.fields_cache = self.__autospector__()

        for k in kwargs:
            if (
                k not in self.fields_cache.keys()
            ):  # on the fly access to obviate the need for gc
                raise UnknownFieldError(
                    f"Key {k} not found in document {type(self).__name__}"
                )
            
            self._data.add(k, kwargs.get(k))

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

    def _presave(self):
        """
        Validates inputs and ensures all required fields and other
        constraints are present before the save operation is called
        """
        for k in self.fields_cache:
            # get a local copy of the field instance
            f = self.fields_cache.get(k)

            # get the value saved in the local data cache
            v = self._data.get(k)

            if not v:
                if f.default:
                    self._data.add(k, f.default)
                    if callable(f.default):
                        self._data.add(k, f.default())
                elif f.required:
                    raise ValidationError(
                        f"{f._name} is a required field of {type(self).__name__}"
                    )

    def save(self):
        """
        Save changes made to document to cloud firestore.
        """
        self._presave()

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
