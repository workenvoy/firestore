from google.cloud.client import Client

# we know that these guys will not be imported with import * as they begin with an underscore
_dbs = {}
_connections = {}


class Connection(object):
    """
    A connection is the link between your project and
    Google Cloud Firestore

    :param connection_string {str}:
    """

    pass
