import pytest
import os

from firestore.db.connector import is_online


FIREBASE_PATH = os.path.abspath(os.path.join(os.path.expanduser("~"), ".ssh/mcr.json"))

IS_LOCAL_ENV = os.environ.get("FIRESTORE_CONFIG", False)


online = pytest.mark.skipif(
    not (is_online() and IS_LOCAL_ENV), reason="Only run this test if internet connectivity is available"
)
