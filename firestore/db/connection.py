import os
from collections import deque

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

from firestore.errors import InvalidDocumentError, DuplicateError, NotFoundError

from google.cloud.firestore_v1.document import DocumentReference

# we know that these guys will not be imported with import * as they begin with an underscore
_dbs = {}
_connections = {}


DEFAULT = "default"
SLASH = "/"
EQUALS = "=="


class ResultSet(object):
    def __init__(self, *args, **kwargs):
        self.__data__ = deque(*args)

    def append(self, result):
        if not isinstance(result, DocumentReference):
            raise InvalidDocumentError("Only documents can be added to a results set")
        self.__data__.append(result)

    def first(self):
        if self.__data__:
            return self.__data__.popleft()

    def next(self):
        return self.first()

    def __bool__(self):
        return bool(self.__data__)


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
        ref = doc.__loaded__
        if ref and isinstance(ref, DocumentReference):
            return doc.__loaded__.delete()
        else:
            raise NotFoundError("Document does not exist")

    def find(self, **kwargs):
        """Perform a query on cloud firestore using key names
        and values present in the default args dict"""
        query_args = {k: kwargs.get(k) for k in kwargs if k not in ("limit")}

        limit = kwargs.get("limit", 10)
        if limit > 100:
            limit = 100

        def query_builder(doc_collection):
            if escape_logic:
                return doc_collection.where()
            return query_builder(query)

        query = query_builder(query_args)
        query = query.limit(limit)

    def get(self, cls, uid):
        """
        Get an instance of the document from firestore if it
        exists and return a result set of the wrapped
        document or an empty result set otherwise
        """
        docref = self._db.document(uid)
        _doc = docref.get()
        if _doc.exists:
            doc = cls(_doc.to_dict())
            doc.__loaded__ = docref
            return ResultSet([doc])
        else:
            return ResultSet()

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
            if cref.document(doc._pk.value).get().exists:
                raise DuplicateError(
                    f"Document with primary key {doc.pk}=`{doc._pk.value}` already exists"
                )
            identifier = cref.document(doc._pk.value)
            identifier.set(doc._data)
            doc.__loaded__ = identifier
        else:
            identifier = cref.document()
            doc.pk = identifier.id
            identifier.set(doc._data)
            doc.__loaded__ = identifier
        return doc
