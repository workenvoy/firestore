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
from firestore.db import Connection
from firestore.errors import (
    InvalidDocumentError,
    UnknownFieldError,
    ValidationError,
    OfflineDocumentError,
)
from google.cloud.firestore_v1 import DocumentReference

# from firestore.datatypes.base import Base
STOP_WORDS = ("the", "is")
DOT = "."
SLASH = "/"
UID = "{}/{}"


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


class Collection(object):
    """Collections are recommended to be used when saving objects
    to firestore. They ensure a schema exists under which data can be
    stored i.e. reducing the error of typing name and naame across
    two different documents.

    They also help to group together commonly used actions across documents
    i.e. setting and saving, querying, and updating document instances.
    """

    # If child documents don't specify a collection
    # then default their location to the root firestore
    # collection

    __collection__ = None

    @classmethod
    def __autospector__(cls, *args, **kwargs):
        return {
            k: v
            for k, v in cls.__dict__.items()
            if k not in ["__module__", "__doc__", "__collection__"]
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
        self._uniques = {}
        self._data = Cache()
        self._parent = self.__collection__
        self.__loaded__ = False
        self.__mutated__ = True

        # Similar to the ._data instance cache. However this
        # is a collection of all descriptor instances
        # that exist on this document class.
        # Useful for pk, unique, required and other document
        # level validation

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

    @classmethod
    def bases(cls):
        _b = list(cls.__bases__)
        for __b in _b:
            _b.extend(__b.__bases__)
        return _b

    @property
    def collection(self):
        """
        Return the class variable
        """
        cls = type(self)
        if not cls.__collection__:
            return cls.__name__.lower()
        return type(self).__collection__.replace(DOT, SLASH)

    @collection.setter
    def collection(self, value):
        """
        Note this changes the class variable
        """
        type(self).__collection__ = value.replace(DOT, SLASH)

    @classmethod
    def count(cls, **kwargs):
        """
        Count the number of records that exist on firestore
        up until 5000 then return 5k+ if records
        exceed that number. The implmentation of this
        method might (will!) change
        """
        pass

    @property
    def dbpath(self):
        if self.__loaded__:
            return self.__loaded__.path  #pylint: disable=no-member
        elif self._pk:
            return UID.format(self.collection, self._pk.value)
        else:
            raise OfflineDocumentError("")

    def delete(self):
        """
        Delete this account by using it's primary key
        or a unique identifier
        """
        conn = Connection.get_connection()
        conn.delete(self)

    @classmethod
    def get(cls, document_id):
        """
        Get a document by its unique identifier on firebase
        """
        conn = Connection.get_connection()
        return conn.get(cls, UID.format(cls().collection, document_id))

    @classmethod
    def find(cls, *args, **kwargs):
        """
        Find a document using the keyward value pairs and limit to
        20 results if no limit key is passed in
        """
        conn = Connection.get_connection()
        return conn.find(cls, *args, **kwargs)

    def get_field(self, field):
        """
        Get a field form the internal _data store of field values
        """
        return self._data.get(field._name)

    def persist(self):
        """Save changes made to this document and any children of this
        document to cloud firestore
        """
        pass

    @property
    def pk(self):
        return self._data._pk

    @pk.setter
    def pk(self, value):
        if self._data._pk:
            raise InvalidDocumentError(
                f"Duplicate primary key `{value._name}` assigned on document "
                f"with existing pk `{self._data._pk}`"
            )
        if isinstance(value, DocumentReference):
            self._data._pk = value.id
        else:
            self._data._pk = value._name

        # Document instances private copy of the primary key field
        # instance for private limited use i.e. in firestore
        # lookup query to match pk name with value
        self._pk = value

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
                elif f.required or f.pk:
                    raise ValidationError(
                        f"{f._name} is a required field of {type(self).__name__}"
                    )

    def save(self):
        """
        Save changes made to document to cloud firestore.
        """
        if not self.__mutated__:
            return
        self._presave()
        conn = Connection.get_connection()
        res = conn.post(self)
        self.__mutated__ = False
        return res

    @classmethod
    def search(cls, query_string, compound_search=False):
        """
        Search for a document using text values. Note this
        is not supported locally by firebase and this library
        uses a read hack to implement text search.
        It is production ready but your mileage might vary.

        @param: query_string {str}
        --------------------------
        This is the text data, search text, or query to use
        as input for the actual search to be done on firestore

        @param: compound_search {bool}
        ------------------------------
        If compound search is enabled then the search terms
        i.e. text used for lookup will be flagged as compound
        before a search is submitted.
        This means all matching documents must have all the words
        in the search text before it returns.
        e.g. red car - only documents with both red and car will be
        returned, documents with only red or only car will
        be ignored

        @return: results {firestore.db.result.Results}
        ----------------------------------------------
        A collection of traversable result documents limited by
        the paginate field which maxes out at 100
        """
        pass

    def transaction(self):
        """
        Perform a transaction i.e. persist all changes or roll back
        entire transaction
        """
        pass

    @property
    def uniques(self):
        """
        Unique fields only hold true if the value is not empty
        i.e. null.
        To prevent null mark the field as required, only fields
        that have a value will be used for the unique evaluation
        """
        return self._uniques

    @uniques.setter
    def uniques(self, values):
        k, v = values
        self._uniques[k] = v
