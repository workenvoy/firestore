import os

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

# we know that these guys will not be imported with import * as they begin with an underscore
_dbs = {}
_connections = {}


class Connection(object):
    """
    A connection is the link between your project and
    Google Cloud Firestore

    :param connection_string {str}:
    """

    def __init__(self, certificate):
        _client = _connections.get("client")
        if _client:
            self._db = _client
        else:
            if certificate:
                self.certificate = credentials.Certificate(certificate)
            firebase_admin.initialize_app(self.certificate)
            self._db = firestore.client()
            _connections["client"] = self._db

    def push(self):
        pass
