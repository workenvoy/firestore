from unittest import TestCase

from firestore import Connection

from firestore.datatypes._special_array import SpecialArray
from firestore import Reference, Collection, String, Array

from tests import online, FIREBASE_PATH


class AnotherDocument(Collection):
    __collection__ = "testdoc"
    first_name = String(pk=True)

class ReferenceDoc(Collection):
    __collection__ = "testref"
    references = Array(Reference(AnotherDocument), minimum=3)


@online
class SpecialArrayTest(TestCase):
    def setUp(self):
        self.sa = SpecialArray(['One', 0, 3, 5, 6, 9, 0, True])

        self.a = AnotherDocument()
        self.bb = AnotherDocument()
        self.ccc = AnotherDocument()

        self.rd = ReferenceDoc()

        self.connection = Connection(FIREBASE_PATH)
    
    def tearDown(self):
        pass
    
    def test_special_array_instantiation(self):
        sa = SpecialArray([num for num in range(10)])
        self.assertEqual(sa, [0,1,2,3,4,5,6,7,8,9])
    
    def test_special_array_index(self):
        self.assertEqual(self.sa.index(True), 7)
    
    def test_special_array_count(self):
        self.assertEqual(self.sa.count(0), 2)
    
    def test_special_array_pop(self):
        popped = self.sa.pop()
        self.assertTrue(popped)
        self.assertIsInstance(popped, bool)
        self.assertEqual(self.sa, ['One', 0, 3, 5, 6, 9, 0])

    def test_special_array_append_ref(self):
    
        self.a.first_name = "special-array"
        self.bb.first_name = "special-arrays"
        self.ccc.first_name = "special-arrayss"

        self.a = self.a.save()
        self.bb = self.bb.save()
        self.ccc = self.ccc.save()

        self.rd = self.rd.save()

        self.rd.references = [self.a, self.bb, self.ccc]

        self.rd = self.rd.save()
        # import pdb; pdb.set_trace()
        self.rd = ReferenceDoc.get(self.rd.pk).first()
        # import pdb; pdb.set_trace()
        self.assertEqual(len(self.rd.references), 3)

        self.assertEqual(self.rd.references[0].id, self.a.pk)

        self.rd.delete()

        self.a.delete()
        self.bb.delete()
        self.ccc.delete()
    
    def test_special_array_append_doc(self):
        pass
    
    def test_special_array_reverse(self):
        pass
