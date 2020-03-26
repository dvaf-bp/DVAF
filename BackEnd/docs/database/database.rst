Database
==========================

database.database
-----------------

To get access to the database layer and logging simply import the
modules like this:

.. code-block::

    from database import db, logger
    result = db.database.collection.find({"attribute": "value"})
    logger.info("blablabla")

:code:`db.database` is an object of type MongoClient. See
https://api.mongodb.com/python/current/api/pymongo/mongo_client.html
for more information.

database.database.Database
---------------------------------

.. automodule:: database.database
    :members:
    :undoc-members:
    :show-inheritance:
