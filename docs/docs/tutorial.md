
In this tutorial we will attempt to introduce you to all the functionality
made available by Firestore Python for building PWAs, APIs, or any other
Python application of your choosing.

In the traditional nature of such tutorials we will be creating a Blog Application called `Fireblog`.

Fireblog is centered around `users`, their `posts`, `comments` on those posts and `files`.

## Installation &amp; Getting Started

First ensure you have [Installed Firestore]() and you have a copy of
your [Google Firestore JSON Certificate]() in an accessible location -- i.e. a location from where your code can read the file in.

    $ pip install firestore

Once you have ensured firestore is installed and the certificate file is
accessible you can start using firestore directly.

## Firestore Concepts

Firestore is a [NoSQL]() database and as such operates under a different set of rules from [Relational]() and [Graph]() databases.

Covering database types is outside the scope of this tutorial -- however, even amongst NoSQL databases e.g. `MongoDB`, `ArangoDB`, `CouchDB` etc.
Firestore is a little bit different in it's core concepts.

For example looking at the image below it is clear that Firestore has a different architectural model from MongoDB (One of the Popular NoSQL Database Engines).

![Firebase v Mongo Diagram](https://res.cloudinary.com/microcessor/image/upload/v1566605839/Open/firestore_v_mongo_ps22gd.png)