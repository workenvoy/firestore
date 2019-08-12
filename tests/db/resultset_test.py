from unittest import TestCase

from firestore import Collection, String

from firestore.db.connection import ResultSet


class QueryDocument(Collection):
    __collection__ = "testaroos"

    name = String(required=True)




class ResultSetTest(TestCase):

    def setUp(self):
        self.rs = ResultSet()
        self.rss = ResultSet([34])
        self.qd = QueryDocument(name="yimu")
    
    def tearDown(self):
        pass
    
    def test_empty_result_set_false(self):
        self.assertFalse(self.rs)
    
    def test_result_set_equal(self):
        self.qd.name = "ayimu"
        doc_one = self.qd.save()
        self.qd.name = "AYIMMMUSSS"
        doc_two = self.qd.save()
        self.assertEqual(doc_one, doc_two)
        doc_two.delete()
    
    def test_find_document(self):
        self.qd.name = "ayimu"
        self.qd.save()
        res = QueryDocument.find(('name', '==', 'ayimu'), limit=3)
        self.assertIsInstance(res, ResultSet)
        self.assertEqual(len(res), 3)
        self.qd.delete()
    
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
