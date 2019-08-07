import os

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

from firestore.errors import InvalidDocumentError, DuplicateError

# we know that these guys will not be imported with import * as they begin with an underscore
_dbs = {}
_connections = {}


DEFAULT = "default"
SLASH = "/"
EQUALS = "=="


class Connection(object):
    """
    A connection is the link between your project and
    Google Cloud Firestore

    :param connection_string {str}:
    """

    def __init__(self, certificate):
        _conn = _connections.get(DEFAULT)
        if _conn:
            self._db = _conn._db
        else:
            if certificate:
                self.certificate = credentials.Certificate(certificate)
            firebase_admin.initialize_app(self.certificate)
            self._db = firestore.client()
            _connections[DEFAULT] = self
    
    def delete(self, doc):
        """
        Remove the doc or the doc with the provided id from
        firestore cloud db if it exists
        """
        pass

    def get(self, doc):
        pass

    @staticmethod
    def get_connection():
        __connection__ = _connections.get(DEFAULT)
        if not __connection__:
            raise ConnectionError(
                "No connection object found, are you sure you"
                "have created a connection with `conn = Connection(firestore_cert)`"
            )
        return __connection__

    def patch(self, doc):
        pass

    def post(self, doc):
        collection_string = doc.collection
        if not collection_string:
            raise InvalidDocumentError("Parent collection not found on document")

        # even numbered collection strings are invalid
        # as they signify a document not a collection
        # i.e. collection.document.subcollection.document
        # and collections or subcollections will always
        # have an odd numbered array length
        if not len(collection_string.split(SLASH)) % 2:
            raise InvalidDocumentError(
                "Invalid collection name, looks like collection ends in a document"
            )

        cref = self._db.collection(collection_string)

        for k in doc.uniques:
            # it is advisable to limit your unique fields in a single firestore
            # document to no more than 5.
            # Every unique field is a read/query to the firestore db to check
            # for a match and thus use unique fields sparingly
            # or not!!! If time and money is of no concern
            v = doc.uniques.get(k)
            if v and [res for res in cref.where(k, EQUALS, v).limit(1).get()]:
                raise DuplicateError(
                    f"Document found in firestore for unique field `{k}` with value `{v}`"
                )

        if doc.pk:
            if cref.document(doc.pk).get().exists:
                raise DuplicateError("Document with primary key already exists")
            identifier = cref.document(doc.pk)
            identifier.set(doc._data)
        else:
            identifier = cref.document()
            doc.pk = identifier.id
            identifier.set(doc._data)
        return identifier
