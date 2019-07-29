"""
    firestore.containers
    ~~~~~~~~~~~~~~~~~~~~

    Containers package used to group class modules
    that enable data to be grouped together under collections
    or documents.

    This package contains only 2 module.Classes [Collection, Document]

    :copyright: 2019 Workhamper
    :license: MIT
"""


from .collection import Collection
from .document import Document


__all__ = [
    'Collection',
    'Document'
]
