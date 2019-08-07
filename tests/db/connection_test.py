import os

from datetime import datetime as clock
from unittest import TestCase
from pytest import mark

from firestore import Connection, Collection, Integer, String, Timestamp
from firestore.db.connection import _connections
from firestore.errors import DuplicateError, InvalidDocumentError, ValidationError

from . import online, FIREBASE_PATH


DEFAULT = "default"


class Account(Collection):
    title = String(required=True, pk=True)
    expires = Timestamp(default=clock.now)


class TestNoConnection(TestCase):
    def test_connection_error_raised(self):
        with self.assertRaises(ConnectionError):
            _ = Connection.get_connection()


@online
class TestConnection(TestCase):
    
    def setUp(self):
        self.connection = Connection(FIREBASE_PATH)
        self.account = Account()
    
    def tearDown(self):
        try:
            self.connection._db.document('whiteboarders/title').delete()
        except:
            pass
    
    def test_firebase_connection(self):
        self.assertEqual(self.connection._db, _connections.get(DEFAULT)._db)
    
    def test_document_created(self):
        self.account.collection = "whiteboarders"
        self.account.title = "xdeletable"
        self.account.save()

        # remember the pk field name is `name`
        doc_ref = self.connection._db.collection('whiteboarders').document(self.account.pk)
        doc_data = doc_ref.get()
        self.assertTrue(doc_data.exists)
    
    def test_account_deleted(self):
        self.account.delete()
    
    def test_invalid_doc_validation_error(self):
        with self.assertRaises(ValidationError):
            self.account.save()

    def test_document_deleted(self):
        self.account.title = "change title"
        self.account.save()
    
    @mark.skip
    def test_document_lookup(self):
        self.account.title = "anothertitle"
        id = self.account.save()
        self.assertEqual
    
    @mark.skip
    def test_document_search(self):
        pass


class BaseDocument(Collection):
    __collection__ = "whiteboarders"
    name = String(unique=True)
    email = String(unique=True)


class BaseDocumentTest(TestCase):
    def setUp(self):
        self.bd = BaseDocument()
        self.connection = Connection(FIREBASE_PATH)
        self.account = BaseDocument()
    
    def tearDown(self):
        pass

    def test_uniques_added_to_document(self):
        self.bd.name = "emailer"
        self.bd.email = "emailer@email.com"

        self.assertEqual(self.bd.uniques, {
            "name": self.bd.name,
            "email": self.bd.email
        })
    
    def test_unique_error_raised(self):
        self.bd.name = "emailer"
        self.bd.email = "emailer@email.com"
        with self.assertRaises(DuplicateError):
            self.bd.save()
