from unittest import TestCase

from firestore import Collection, String
from firestore.errors import ValidationError
from firestore.containers.collection import Cache


class StringDocument(Collection):
    name = String(required=True, minimum=5, maximum=10)
    email = String(coerce=False)


class StringTest(TestCase):
    """
    Tests for the String firestore datatype/field class
    """

    def setUp(self):
        self.sd = StringDocument()

    def tearDown(self):
        pass

    def test_string_minimum(self):
        with self.assertRaises(ValidationError):
            self.sd.name = "me"
        with self.assertRaises(ValidationError):
            self.sd.name = "very very very very long name"
        with self.assertRaises(ValidationError):
            self.sd.name = 5
    
    def test_string_coerce(self):
        with self.assertRaises(ValueError):
            self.sd.email = 5

    def test_string_in_collection_document(self):
        self.sd.name = "Whosand"
        expecting = Cache()
        expecting.add("name", "Whosand")
        self.assertEqual(expecting, self.sd._data)
