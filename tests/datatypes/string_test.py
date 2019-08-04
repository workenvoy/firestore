from unittest import TestCase

from firestore import Document, String
from firestore.errors import ValidationError
from firestore.containers.document import Cache


class StringDocument(Document):
    name = String(required=True, minimum=5, maximum=10)


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

    def test_string_in_document(self):
        self.sd.name = "Whosand"
        expecting = Cache()
        expecting.add("name", "Whosand")
        self.assertEqual(expecting, self.sd._data)
