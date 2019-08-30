from unittest import TestCase

from firestore import Document, Connection
from firestore import String, Integer

from tests import online, FIREBASE_PATH


class Parent(Document):
    __collection__ = "testdoc"

    uid = String(pk=True)
    name = String(required=True)
    age = Integer(required=True, minimum=40)

class Child(Document):
    __collection__ = "testdoc/{}/child"

    uid = String(pk=True)
    name = String(required=True)
    age = Integer(required=True, minimum=18)

class Grandchild(Document):
    __collection__ = "testdoc/{}/child/{}/grandchild"

    uid = String(pk=True)
    name = String(required=True)
    age = Integer(required=True)


@online
class ResolutionTest(TestCase):
    def setUp(self):
        PARENT = "100"
        CHILD = "200" 
        GRAND_CHILD = "300"

        self.parent = Parent()
        self.child = Child()
        self.grand_child = Grandchild()

        self.connection = Connection(FIREBASE_PATH)

        self.parent.uid = PARENT
        self.parent.name = type(self.parent).__name__
        self.parent.age = 50
        self.parent.save()

        self.child.uid = CHILD
        self.child.name = type(self.child).__name__
        self.child.age = 30

        self.child.save(PARENT)
        
        self.grand_child.uid = GRAND_CHILD
        self.grand_child.age = 4
        self.grand_child.name = type(self.grand_child).__name__

        self.grand_child.save(CHILD, PARENT)

    
    def tearDown(self):
        self.parent.delete()
        self.child.delete()
        self.grand_child.delete()
    
    def test_collection_name_resolution(self):
        """
        Resolve placeholders on collection into dynamic id's and
        return fully qualified sub collection path urls
        """
        self.assertEqual(self.parent.collection, "testdoc")
        self.assertEqual(self.child.collection, "testdoc/100/child")
        self.assertEqual(self.grand_child.collection, "testdoc/100/child/200/grandchild")

        self.assertEqual(self.grand_child, Grandchild.get("300", "200", "100").first())
