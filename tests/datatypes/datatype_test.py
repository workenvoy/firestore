from unittest import TestCase

from firestore import Collection, Datatype
from firestore.errors import ValidationError


class DatatypeDoc(Collection):
    first_name = Datatype("sTring", required=True, coerce=False)



class DatatypeTest(TestCase):

    def setUp(self):
        self.dd = DatatypeDoc()
    
    def tearDown(self):
        pass
    
    def test_datatype_returns_appropriate_field_type(self):
        with self.assertRaises(ValueError):
            self.dd.first_name = 5
