from unittest import TestCase
from pytest import mark

from firestore import Collection, Reference, String


class AnotherDocument(Collection):
    first_name = String(required=True)


class ReferenceDocument(Collection):
    reference = Reference(AnotherDocument)

class UnrelatedDocument(Collection):
    ref = Reference('ReferenceDocument')


class TestReference(TestCase):
    def setUp(self):
        self.rd = ReferenceDocument()
        self.urd = UnrelatedDocument()
    
    def tearDown(self):
        pass
    
    def test_reference_assignment_error(self):
        with self.assertRaises(AttributeError):
            self.rd.reference = UnrelatedDocument()
    
    def test_reference_assignment(self):
        _ = AnotherDocument()
        self.rd.reference = _
        self.assertEqual(self.rd.reference, _)
    
    @mark.skip
    def test_string_reference(self):
        # When str dereferencing is not implemented this
        # throws a type error when validating because
        # ReferenceDocument() instance can not be
        # compared to isinstance(RefDoc(), "string").
        # isinstance expects type not "" which makes
        # this test ideal to test deref is correctly implemented
        self.urd.ref = ReferenceDocument()

        # after implementing deref above assert below here
    
    def test_reference_document_string(self):
        pass
