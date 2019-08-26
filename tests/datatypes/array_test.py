from unittest import TestCase

from firestore import Array, Collection
from firestore.containers.collection import Cache

from firestore.errors import ValidationError


class ArrayDocument(Collection):
    children_ages = Array(minimum=3, maximum=5)


class TestArray(TestCase):
    def setUp(self):
        self.ad = ArrayDocument()
        self._ = [5, 10, 'Yes', True]
    
    def tearDown(self):
        pass
    
    def test_array_in_collection_document(self):
        self.ad.children_ages = self._
        cache = Cache()
        cache.add("children_ages", self._)
        self.assertEqual(self.ad._data, cache)
    
    def test_array_boundary_exceptions(self):
        with self.assertRaises(ValidationError):
            self.ad.children_ages = self._ + ['You', None]
        with self.assertRaises(ValidationError):
            self.ad.children_ages = ['a']
