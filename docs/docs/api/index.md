
# Datatypes

Datatypes are the fundamental units of storage of your ORM.

## Arrays

Arrays are synonymous to lists in Python

## Booleans

True or False Values represented by the `firestore.datatypes.boolean.Boolean` class. Boolean values are coercible from other python types i.e. `0, "", []` = False, `1, "*", [1]` = True.

## Collection

Collections are groupings of documents i.e. Documents are instances of data and collections are
the houses under which these documents are grouped or live.

Following the example blog post - Blog is a Collection and a Document because the collection name is called Blog and the Python Blog Class represents a single Document that will be saved to Google Cloud Firestore.

```python

from firestore import Document
from firestore import Collection, String

class User(Document):
    __collection__ = "users"

    name = String()
    email = String(regex="some email regex")


class Comment(Document):
    __collection__ = "users/{}/blog/{}/comments"

    made_by = Reference(User)


class Blog(Document):
    __collection__ = "users/{}/blog"

    name = String()
    comments = Collection(Comment)

```

Here `Blog.comments` will hold a [Google Cloud Firestore Subcollection](https://firebase.google.com/docs/firestore/data-model#subcollections) of `Comment` Documents.


## Document Class Meta Attributes

You might have noticed some squiggly class attributes `__****__` in our Document definitions.
These are Python Firestore specific meta attributes.

### `__collection__`
This is an **Optional Meta Attribute** i.e. You don't need to provide it if the Document will live in a root collection e.g. `/users` or `/countries`. The same holds true for subcollections that will not be saved outside their parent Documents

    class Comment(Document):
        #no __collection__ meta declared here
        text = String()
        commented_on = Timestamp()
    
    class Post(Document):
        # no __collection__ meta declared here as well
        comments = Collection(Comment)


    # This is perfectly fine as long as you don't use comment
    # outside of its parent Post Class
    comment = Post.comments.new()
    # or
    p = Post.get("some_post_id")
    comment = p.comments.new()


    # This will not raise an error but instead save comment
    # in the root collection `/comment` and might not
    # be what you expected
    comment = Comment()
    comment.text = "I like this post"
    comment.save()


The Collection Meta Attribute is parsed according to the following rules:

* `/post` or `post` - The document will be saved in a root collection called **post**
* `post/{}/comments` - The `{}` is a placeholder into which Python Firestore inserts Unique Document IDs i.e. This collection url therefore implies that all child **documents** of the root `post` collection will have a `comment` **subcollection**. 



### `__uniques__`