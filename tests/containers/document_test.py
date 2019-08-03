from unittest import TestCase

from firestore import Document, String
from firestore.containers.document import Cache

MOUTHFUL = "supercalifragiexpialiantidocious"


class DocumentTest(TestCase):
    
    def setUp(self):
        class TestDocument(Document):
            yimu = String(required=True)
        
        self.td = TestDocument()
    
    def tearDown(self):
        pass
    
    def test_cache(self):
        cache = Cache()
        cache.name = MOUTHFUL
        self.assertEqual(cache.name, MOUTHFUL)

        self.assertLessEqual({"_pk": False}.items(), cache.items())

    def test_cache_persists_correctly(self):
        self.td.yimu = "true"
        expected = {"type": str, "value": "true", "required": True}
        self.assertEqual(self.td._data.yimu, expected)
