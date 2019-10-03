from unittest import TestCase

from firestore import Collection, String, Integer, Reference, Map, Array, MapSchema


class SchemaCollection(Collection):
    __schema__ = ["name"]
    name = String(required=True, minimum=5, help_text="Name", maximum=10)
    age = Integer(unique=True)
    scores = Array()


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
        res = sc.get_json_schema()
        
        self.assertEquals(res, {
            "name": {
                "help_text": "Name",
                "datatype": "String",
                "required": True,
                "minimum": 5,
                "maximum": 10
            },
            "age": {
                "datatype": "Integer",
                "unique": True
            },
            "scores": {
                "datatype": "Array"
            }
        })
