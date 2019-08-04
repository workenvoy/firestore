from unittest import TestCase
from datetime import timedelta, timezone, datetime as clock

from firestore import Document, Integer, String, Timestamp
from firestore.containers.document import Cache


class TimestampDocument(Document):
    created_date = Timestamp(default=clock.now)
    age = Integer(minimum=5, required=True)
    email = String(unique=True)

    def do_nothin_special(self):
        ''''''
        pass


class TimestampTest(TestCase):
    def setUp(self):
        self.td = TimestampDocument()
        self._ = clock.now(tz=timezone.utc)

    def tearDown(self):
        pass

    def test_timestamp_in_document(self):

        self.td.created_date = self._
        expected = Cache()
        expected.add("created_date", self._)
        self.assertEqual(expected, self.td._data)

    def test_only_valid_types_allowed(self):
        with self.assertRaises(ValueError):
            self.td.created_date = "You"
