from unittest import TestCase

from firestore import Collection, String, Integer, Reference, Map, Array, MapSchema


class SchemaCollection(Collection):
    __schema__ = ["name"]

class NoneSchemaCollection(Collection):
    pass


class SchemaTest(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_schema_is_none(self):
        nsc = NoneSchemaCollection()
        self.assertIsNone(nsc.__schema__)
    
    def test_schema_is_not_none(self):
        sc = SchemaCollection()
        self.assertIsNotNone(sc.get_json_schema())
