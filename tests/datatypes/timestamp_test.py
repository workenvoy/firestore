from unittest import TestCase
from datetime import timedelta, timezone, datetime as clock

from firestore import Document, Integer, String, Timestamp
from firestore.containers.document import Cache

from firestore.errors import ValidationError


class TimestampDocument(Document):
    created_date = Timestamp(default=clock.now)
    last_modified = Timestamp(minimum="2019-10-20")
    active_until = Timestamp(maximum="2020")
    expiry_date = Timestamp(minimum=1609459200)  # timestamp for 2021

    def do_nothin_special(self):
        """"""
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
            self.td.created_date = "you"
    
    def test_coerces_minimum(self):
        with self.assertRaises(ValidationError):
            self.td.last_modified = "2019-10-19"
        with self.assertRaises(ValidationError):
            self.td.expiry_date = '2017'
    
    def test_coerces_maximum(self):
        with self.assertRaises(ValidationError):
            self.td.active_until = 1609459200.28904  # timestamp for 2021 ->