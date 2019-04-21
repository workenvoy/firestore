

from firestore import connection
from firestore import Repository
from firestore import String
from firestore import Date
from firestore import Integer
from firestore import Relationship


from firestore.lazy import Datatype

class Storing(Repository):
    __collection__ = "collection-name"

    firstname = String(required=True)
    lastname = Datatype(datatype="StRiNg")  # case does not matter when describing datatypes
    middlename = Datatype("string")  # you can also omit the parameter name


# returns the first occurence it finds even if 20 exists or None if nothing found
# when multiple filters are used it becomes an and operation i.e. contains something and equals something
storing = Storing.find(key="firstname", contains="something", icontains="something", equals="something")
storing = Storing.get()  # same thing but without an argument gets the first item pass -1 to get the last item or 4 to get the 4th

# gets all the documents and even if only one document is found it returns it in a query object i.e. [query_object]
# that has the same interface as a default python list
storings = Storing.gets(firstname__contains="something")
storings = Storing.finds()
storings = Storing.finds(paginate=25, index=-1)  # get from last item to 24 items before last item

someDate = ""
someOtherDate = ""  # ideally these should be dates
storings_between_dates = Storing.finds(start_date=someDate, end_date=someOtherDate)  # if you use naive dates then it matches the timezone stored in the db else it converts to the timezone db and returns a value


# Documents have limits - max size is 1mb including the maps in a document
# You can't retrieve a partial document, so retrieving only title is not an option and you retrieve all other fields
# Queries are shallow : you won't get sub-collections with a query only the parent and no children
# You are billed by the number of reads and writes you make - read and write sensibly
# Queries find documents in collections - no querying across collections or wait-for-it `sub-collections`
# Arrays are weird
