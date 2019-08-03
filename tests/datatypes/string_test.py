from unittest import TestCase

from firestore.errors import ValidationError
from firestore import Document
from firestore import String



class StringTest(TestCase):
    """
    Tests for the String firestore datatype/field class
    """

    def setUp(self):
        class TestStringClass(Document):
            name = String(required=True, minimum=5, maximum=10)
        self.tc = TestStringClass()
    
    def tearDown(self):
        pass

    def test_string_minimum(self):
        with self.assertRaises(ValidationError):
            self.tc.name = "me"
        with self.assertRaises(ValidationError):
            self.tc.name = "very very very very long name"
