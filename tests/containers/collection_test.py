from unittest import TestCase
from pytest import mark

from firestore import Collection as Document, String

from firestore.errors import InvalidDocumentError, ValidationError, UnknownFieldError
from firestore.containers.collection import Cache

MOUTHFUL = "supercalifragiexpialiantidocious"

YDS = "yabba/dooda/speca"


class DuplicateDoc(Document):
    field = String(pk=True)
    field2 = String(pk=True)

class ConstructorDocument(Document):
    __collection__ = "yabba.dooda.speca"
    name = String(required=True, unique=True, pk=True)

class TheDocument(Document):
    yimu = String(required=True)

class RequiredDocument(Document):
    email = String(required=True)
    first_name = String(required=True)
    last_name = String(required=True)

class DocumentTest(TestCase):
    def setUp(self):
        self.td = TheDocument()
        self.dd = DuplicateDoc()
        self.rd = RequiredDocument()
        self.cd = ConstructorDocument(name="Yessiree")

    def tearDown(self):
        pass
    
    def test_collection_name(self):
        self.assertEqual(self.cd.collection, YDS)
    
    def test_set_collection_name(self):
        self.cd.collection = "booting"
        # here we are testing the instance proxied the value to the
        # class correctly thus we access the class variable directly
        # to check
        self.assertEqual(type(self.cd).__collection__, "booting")

    def test_cache(self):
        cache = Cache()
        cache.name = MOUTHFUL
        self.assertEqual(cache.name, MOUTHFUL)

        self.assertLessEqual({"_pk": False}.items(), cache.items())

    def test_cache_persists_correctly(self):
        self.td.yimu = "true"
        self.assertEqual(self.td._data.yimu, self.td.yimu)

    def test_recursive_cache_access(self):
        pass

    def test_document_has_instance(self):
        self.td.yimu = "true"
        expected = {
            "_pk": False,
            "yimu": "true"
        }
        self.assertEqual(self.td._data, expected)

    def test_duplicate_pk(self):
        with self.assertRaises(InvalidDocumentError):
            self.dd.field = "You"
            self.dd.field2 = "You"
    
    def test_dbpath(self):
        _ = "gherkin"
        self.cd.name = _
        self.assertEqual(self.cd.dbpath, "{}/{}".format(YDS, _))
    
    def test_document_constructor_error_for_unknown_key(self):
        with self.assertRaises(UnknownFieldError):
            _ = RequiredDocument(shoe_size=45)
    
    def test_document_constructor_initialization(self):
        self.assertEqual(self.cd.name, "Yessiree")
    
    def test_document_save(self):
        with self.assertRaises(ValidationError):
            self.rd = RequiredDocument()
            self.rd.save()
