"""
Firestore
---------

Firestore is an offline available ODM/OCM for Google Firestore Database
"""
import sys
from setuptools import setup


major, minor = sys.version_info.major, sys.version_info.minor


if(major == 2 and minor < 7) or (major == 3 and minor < 4):
    print("Python 2 E.O.L < 6 months away. This lib only supports Python 3")

dependencies = [
    "google-cloud-firestore"
]


try:
    with open('README.rst') as fin:
        LONG_DESCRIPTION = fin.read()
except Exception:
    LONG_DESCRIPTION = "Firstore Offline-Available ORM/ODM for Google Cloud Firestore DB"


setup(
    name="firestore",
    version="0.0.3",
    description="An offline-available ORM-like wrapper for Google Firestore Database",
    author="Workhamper",
    author_email="raymond@workhamper.com",
    url="https://github.com/workenvoy/firestore",
    packages=['firestore'],
    license="MIT",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database"
    ],
    dependencies=dependencies,
)
