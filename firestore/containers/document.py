"""
    firestore.containers.document
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Documents are the secondary unit of storage. They are the primary
    containers under which data is stored.
    Using the fundamental units of storage such as text, numbers, arrays etc.
    to capture information; this captured information is grouped together
    under documents.

    :copyright: 2019 Workhamper
    :license: MIT
"""


class Document(object):
    """Documents are recommended to be used when saving objects
    to firestore. They ensure a schema exists under which data can be
    stored i.e. reducing the error of typing name and naame across
    two different documents.

    They also help to group together commonly used actions across documents
    i.e. setting and saving, querying, and updating document instances.
    """
    pass
