from unittest import TestCase


from firestore import Collection, Geopoint
from firestore.errors import ValidationError


class GeopointDoc(Collection):
    location = Geopoint()


class GeopointTest(TestCase):

    def setUp(self):
        self.gd = GeopointDoc()
    
    def tearDown(self):
        pass
    
    def test_geopoint_in_collection_document(self):
        self.gd.location = 90, 45
        self.assertEqual(self.gd.location, (90, 45))
        self.assertEqual(self.gd._data, {"_pk": False, "location": (90, 45)})
    
    def test_geopoint_default_values_error(self):
        with self.assertRaises(ValueError):
            class GeopointDocument(Collection):
                location = Geopoint(default=(-180.3, 56.34))
    
    def test_geopoint_validation(self):
        with self.assertRaises(ValueError):
            self.gd.location = 185, 87
        
        with self.assertRaises(ValueError):
            self.gd.location = 89.98721, 180.001
    
    def test_geopoint_invalid_values(self):
        with self.assertRaises(ValueError):
            self.gd.location = 90, "string"
    
    def test_geopoint_assignment(self):
        self.gd.location = 87.233, 141.389
        self.assertEqual(self.gd.location, (87.233, 141.389))
