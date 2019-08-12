from unittest import TestCase, skipUnless, skipIf
import pytest


from . import online


@online
class ConnectionTest(TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_something_real_quick(self):
        pass
