from unittest import TestCase

from firestore import Document, Integer, Map, String
from firestore.datatypes.map import MapSchema


class Mapping(MapSchema):
    name = String(required=True)
    age = Integer(minimum=4)


class MapDocument(Document):
    map = Map(required=True)


class MapTest(TestCase):
    def setUp(self):
        self.md = MapDocument()

    def tearDown(self):
        pass

    def test_map_schema(self):
        """Tests that the map schema object correctly transforms
        to a python dict in the document instance and vis a vis"""
        pass

    def test_map_in_document_instance(self):
        """Test when we create a map it get's loaded into the parent doc instance"""
        self.md.map = {}
