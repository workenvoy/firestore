from unittest import TestCase

from firestore import Connection
from firestore import Collection, String

from firestore.db.connection import ResultSet

from tests import online, FIREBASE_PATH


class QueryDocument(Collection):
    __collection__ = "testaroos"

    name = String(required=True)



@online
class ResultSetTest(TestCase):

    def setUp(self):
        self.connection = Connection(FIREBASE_PATH)
        self.rs = ResultSet()
        self.rss = ResultSet([34])

        self.persisted = QueryDocument(name="persisted").save()

        self.one = QueryDocument(name="yimu").save()
        self.two = QueryDocument(name="yimu").save()
        self.three = QueryDocument(name="yimu").save()
        self.four = QueryDocument(name="yimu").save()
    
    def tearDown(self):
        self.one.delete()
        self.two.delete()
        self.three.delete()
        self.four.delete()
        self.persisted.delete()
    
    def test_empty_result_set_false(self):
        self.assertFalse(self.rs)
    
    def test_result_set_equal(self):
        self.persisted.name = "ayimu"
        doc_one = self.persisted.save()
        self.persisted.name = "AYIMMMUSSS"
        doc_two = self.persisted.save()
        self.assertEqual(doc_one, doc_two)
    
    def test_find_document(self):
        res = QueryDocument.find(('name', '==', 'yimu'), limit=3)
        self.assertIsInstance(res, ResultSet)
        self.assertEqual(len(res), 3)
    
    def test_non_empty_result_set_true(self):
        self.assertTrue(self.rss)

    def test_result_set_next(self):
        let = 0
        out = None

        while self.rss:
            out = self.rss.next()
            if let > 3:  # safety net to prevent infinite loop before first test run
                break
            let += 1
        
        self.assertEqual(out, 34)
        self.assertEqual(let, 1)
