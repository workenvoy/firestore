from unittest import TestCase


from firestore import Boolean, Collection
from firestore.containers.collection import Cache


class BooleanDocument(Collection):
    is_verified = Boolean(default=False, required=False)


class BooleanTest(TestCase):
    def setUp(self):
        self.bd = BooleanDocument()

    def tearDown(self):
        pass

    def test_boolean_in_document_instance(self):
        self.bd.is_verified = True
        expected = Cache()
        expected.add("is_verified", True)
        self.assertEqual(expected, self.bd._data)
