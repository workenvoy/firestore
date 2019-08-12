import os

from datetime import datetime as clock
from unittest import TestCase
from pytest import mark

from firestore import Connection, Collection, Integer, String, Timestamp
from firestore.db.connection import _connections
from firestore.errors import DuplicateError, InvalidDocumentError, ValidationError, NotFoundError

from . import online, FIREBASE_PATH


DEFAULT = "default"
LOOKUP_TITLE = "updatedtitless"


class Account(Collection):
    __collection__ = "whiteboarders"
    title = String(required=True, pk=True)
    expires = Timestamp(default=clock.now)


class Whiteboarders(Collection):
    title = String(pk=True)


class TestNoConnection(TestCase):
    def test_connection_error_raised(self):
        with self.assertRaises(ConnectionError):
            _ = Connection.get_connection()


@online
class TestConnection(TestCase):
    
    def setUp(self):
        self.connection = Connection(FIREBASE_PATH)
        self.wb = Whiteboarders()
        self.account = Account()
        self.titular = Account()
    
    def tearDown(self):
        # self._title.delete()
        try:
            self.connection._db.document('whiteboarders/changetitle').delete()
            self.connection._db.document('whiteboarders/xdeletable').delete()
        except:
            pass
    
    def test_firebase_connection(self):
        self.assertEqual(self.connection._db, _connections.get(DEFAULT)._db)
    
    def test_document_created(self):
        self.account.collection = "whiteboarders"
        self.account.title = "xdeletable"
        self.account.save()

        # remember the pk field name is `name`
        doc_ref = self.connection._db.collection('whiteboarders').document(self.account._pk.value)
        doc_data = doc_ref.get()
        self.assertTrue(doc_data.exists)
    
    def test_account_deleted_error(self):
        with self.assertRaises(NotFoundError):
            self.account.delete()
    
    def test_invalid_doc_validation_error(self):
        with self.assertRaises(ValidationError):
            self.wb.save()

    def test_document_deleted(self):
        self.account.title = "changetitle"
        _ref = self.account.save()
        self.assertTrue(_ref.__loaded__)

        # id attribute provided by firestore cloud ref document
        self.assertEqual(_ref.__loaded__.id, "changetitle")

        load_account = Account.get("changetitle")
        self.assertTrue(load_account)  # i.e. it loaded

        load_account.first().delete()
        self.assertFalse(Account.get("changetitle"))

    def test_document_get_lookup(self):
        self.titular.title = LOOKUP_TITLE
        _ref = self.titular.save()
        res = Account.get(LOOKUP_TITLE)
        self.assertTrue(res)

        # possible as saved _ref account object will now
        # have the __loaded__ ref to cloud firestore docref
        _ref.__loaded__.delete()
    
    @mark.skip
    def test_document_search(self):
        pass


class BaseDocument(Collection):
    __collection__ = "whiteboarders"
    name = String(unique=True)
    email = String(unique=True)

class Zulu(Collection):
    name = String(pk=True)

@online
class BaseDocumentTest(TestCase):
    def setUp(self):
        self.bd = BaseDocument()
        self.connection = Connection(FIREBASE_PATH)
        self.account = BaseDocument()
        self.cp = Zulu()
    
    def tearDown(self):
        try:
            self.connection._db.document('zulu/ghyusdaisds').delete()
        except:
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
            self.bd.name = "emailer"
            self.bd.email = "emailer@email.com"
            self.bd.save()
    
    def test_collection_path_generation(self):
        self.cp.name = "ghyusdaisds"
        self.cp.age = 45
        self.cp.save()
