"""
    firestore.containers.document
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    John Cleese (Commentator): Ah no, they're not. No they didn't realize
    they were supposed to start. Never mind, we'll soon sort that out, the
    judge is explaining it to them now. I think Nigel and Gervaise have
    got the idea. All set to go.

    :copyright: 2019 Workhamper
    :license: MIT
"""


class Cache(dict):
    """
    A class to make attribute lookup and writing
    swift and fast without the need for attribute access
    notation instead defaulting to object access notation
    """
    def __init__(self, *args, **kwargs):
        self._pk = False
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, key):
        # less error prone
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = {
            type: type(value),
            "value": value,
            "required": True
        }
    
    def set(self, key, value, required=False):
        self[key] = {
            "type": type(value),
            "value": value,
            "required": required
        }


class Document(object):
    """Documents are recommended to be used when saving objects
    to firestore. They ensure a schema exists under which data can be
    stored i.e. reducing the error of typing name and naame across
    two different documents.

    They also help to group together commonly used actions across documents
    i.e. setting and saving, querying, and updating document instances.
    """

    def __init__(self, *args, **kwargs):
        """
        Root document holding all the utility methods
        needed for persistence to cloud firestore
        """
        self._data = Cache()
    
    def add_field(self, field, value):
        """Add a field to this instance's data for persistence
        taking into cognizance all the validations present on the field
        """
        self._data[field._name] = value
    
    def save(self):
        """
        Save changes made to document to cloud firestore.
        """
        pass
    
    def persist(self):
        """Save changes made to this document and any children of this
        document to cloud firestore
        """
        pass
    
    def transaction(self):
        """
        Perform a transaction i.e. persist all changes or roll back
        entire transaction
        """
        pass
