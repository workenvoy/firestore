"""
    firestore.containers
    ~~~~~~~~~~~~~~~~~~~~

    Containers package used to group class modules
    that enable data to be grouped together under collections
    or documents.

    This package contains only 2 module.Classes [Collection, Document]


    John Cleese (Commentator): Good afternoon and welcome to Hurlingham Park.
        You join us just as the competitors are running out onto
        the field on this lovely winter's afternoon here, with the going
        firm underfoot and very little sign of rain. Well it certainly
        looks as though we're in for a splendid afternoon's sport in this the
        127th Upperclass Twit of the Year Show. Well the competitors will
        be off in a moment so let me just identify for you.
        (...continued in firestore.containers.collection.py)

    :copyright: 2019 Workhamper
    :license: MIT
"""


from firestore.containers.collection import Collection
from firestore.containers.document import Document

__all__ = ["Collection", "Document"]
