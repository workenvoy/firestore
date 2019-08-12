from unittest import TestCase

from firestore import Collection, Float, Integer
from firestore.containers.collection import Cache

from firestore.errors import ValidationError


class IntegerDocument(Collection):
    age = Integer(minimum=5, maximum=50)


class IntegerCoercedDocument(Collection):
    age = Integer(coerce=True)


class FloatDocument(Collection):
    percentage = Float(minimum=50.0, maximum=100.0)


class IntegerTest(TestCase):
    def setUp(self):
        self.id = IntegerDocument()

    def tearDown(self):
        pass

    def test_integer_in_collection_document(self):
        self.id.age = 5
        expected = Cache()
        expected.add("age", 5)
        self.assertEqual(expected, self.id._data)

    def test_integer_minimum(self):
        with self.assertRaises(ValidationError):
            self.id.age = 1

    def test_integer_maximum(self):
        with self.assertRaises(ValidationError):
            self.id.age = 51

    def test_integer_gets_correctly(self):
        self.id.age = 21
        self.assertEqual(self.id.age, 21)

    def test_integer_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.id.age = "yimu"
        with self.assertRaises(ValueError):
            self.id.age = []

    def test_coercion_false_error(self):
        with self.assertRaises(ValueError):
            self.id.age = 4.0


class FloatTest(TestCase):
    def setUp(self):
        self.fd = FloatDocument()

    def test_float_in_document(self):
        self.fd.percentage = 50.0
        expected = Cache()
        expected.add("percentage", 50.0)
        self.assertEqual(expected, self.fd._data)

    def test_float_minimum(self):
        with self.assertRaises(ValidationError):
            self.fd.percentage = 1.0

    def test_float_maximum(self):
        with self.assertRaises(ValidationError):
            self.fd.percentage = 100.1

    def test_float_gets_correctly(self):
        self.fd.percentage = 21
        self.assertEqual(self.fd.percentage, 21)

    def test_float_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.fd.percentage = "yimu"
        with self.assertRaises(ValueError):
            self.fd.percentage = []
