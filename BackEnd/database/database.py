"""
DVAF -  offers the security-research community with up-to-date information
        about vulnerability trends, types, etc.

Copyright (C) 2019-2020
Nikolaos Alexopoulos <alexopoulos@tk.tu-darmstadt.de>,
Lukas Hildebrand <lukas.hildebrand@stud.tu-darmstadt.de>,
Jörn Schöndube <joe.sch@protonmail.com>,
Tim Lange <tim.lange@stud.tu-darmstadt.de>,
Moritz Wirth <mw@flanga.io>,
Paul-David Zürcher <mail@pauldavidzuercher.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
"""
import pymongo
from database import dbConfig
import logging


class Database:
    def __init__(self):
        self.connected = False
        self.config = dbConfig.DBConfig()
        self.logger = logging.getLogger(__package__)
        self.logger.info("trying to connect to database")

        try:
            self.client = pymongo.MongoClient(
                port=self.config.props.port)
            self.database = self.client
            self.connected = True
            self.logger.info("connection to database established")
        except Exception as e:
            self.logger.fatal("connection to database failed: {}".format(e))

    def close(self):
        self.client.close()

    def is_connected(self):
        return self.connected

    def insert_object(self, collection_name, serializable):
        # check if collection exists
        if collection_name not in self.database.admin.collection_names():
            self.database.admin.create_collection(collection_name)

        collection = self.database.admin.get_collection(collection_name)
        primary_key_name = serializable.get_primary_key_name()

        # check if index exists and is correct
        if [primary_key_name] != collection.index_information().keys():
            collection.drop_indexes()
            collection.create_index(primary_key_name, unique=True)

        # insert
        collection.insert(serializable.to_dict())


# TODO: maybe move this in a different module
def init_database():
    """This function can be called to setup some of the few databases
    and collections."""
    db = Database()

    # cvedb gets built by cve search

    # debian specific stuff
    db.database.debian.packages.create_index("pkg_name", unique=True)

    # dsa indices
    dsa_id_index = pymongo.IndexModel("dsa_id")
    packages_index = pymongo.IndexModel("packages")
    date_index = pymongo.IndexModel("date")
    db.database.debian.dsas.create_indexes([dsa_id_index,
                                            packages_index,
                                            date_index])

    # dla indices
    dla_id_index = pymongo.IndexModel("dla_id")
    packages_index = pymongo.IndexModel("packages")
    date_index = pymongo.IndexModel("date")
    db.database.debian.dlas.create_indexes([dla_id_index,
                                            packages_index,
                                            date_index])
