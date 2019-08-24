from unittest import TestCase
from pytest import mark

from firestore import Collection, Reference, String

from tests import online


class AnotherDocument(Collection):
    first_name = String(pk=True)

class ReferenceDocument(Collection):
    reference = Reference(AnotherDocument)

class UnrelatedDocument(Collection):
    ref = Reference(ReferenceDocument)

@online
class TestReference(TestCase):
    def setUp(self):
        self.ad = AnotherDocument()
        self.rd = ReferenceDocument()
        self.urd = UnrelatedDocument()
    
    def tearDown(self):
        pass

    def test_reference_assignment_error(self):
        self.ad.first_name = "YimuGoba"
        with self.assertRaises(AttributeError):
            self.rd.reference = UnrelatedDocument()

    def test_reference_assignment(self):
        _ = AnotherDocument()
        _.first_name = "test reference assignment"
        self.rd.reference = _
        self.assertEqual(self.rd.reference, _)

    def test_string_reference(self):
        # When str dereferencing is not implemented this
        # throws a type error when validating because
        # ReferenceDocument() instance can not be
        # compared to isinstance(RefDoc(), "string").
        # isinstance expects type not "" which makes
        # this test ideal to test deref is correctly implemented
        self.urd.ref = ReferenceDocument()

        # after implementing deref above assert below here
        self.assertEqual(self.urd, ReferenceDocument)
    
    def test_reference_document_string(self):
        pass
