

from distutils.core import setup


try:
    with open('README.rst') as fin:
        LONG_DESCRIPTION = fin.read()
except Exception:
    LONG_DESCRIPTION = "Firstore Offline-Available ORM/ODM for Google Cloud Firestore DB"


setup(
    name="firestore",
    version="0.1dev",
    packages=['firestore'],
    license='MIT',
    long_description=LONG_DESCRIPTION
)
