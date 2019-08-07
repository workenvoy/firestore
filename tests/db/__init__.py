import pytest
import os

from firestore.db.connector import is_online


FIREBASE_PATH = os.path.abspath(os.path.join(os.path.expanduser("~"), ".ssh/mcr.json"))


online = pytest.mark.skipif(
    not is_online(), reason="Only run this test if internet connectivity is available"
)
