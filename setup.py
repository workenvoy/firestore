"""
Firestore
---------

Firestore is an offline available ODM/OCM for Google Firestore Database
"""

from distutils.core import setup


try:
    with open('README.rst') as fin:
        LONG_DESCRIPTION = fin.read()
except Exception:
    LONG_DESCRIPTION = "Firstore Offline-Available ORM/ODM for Google Cloud Firestore DB"


setup(
    name="firestore",
    version="0.0.1",
    description="An offline-available ORM-like wrapper for Google Firestore Database",
    author="Workenvoy",
    author_email="raymond@workenvoy.com",
    url="https://github.com/workenvoy/firestore",
    packages=['firestore'],
    license="MIT",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "License :: MIT License",
        "Topic :: Database"
    ],
)
