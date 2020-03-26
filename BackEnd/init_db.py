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
from datetime import datetime

import pymongo

from collectors import logger
from collectors.DLACollector import DLACollector
from collectors.DSACollector import DSACollector
from collectors.debian_aliases import insert_debian_package_name_aliases
from collectors.pkg_data_collector import PackageCollector
from collectors.deb_sec_tracker import download_debian_security_tracker_json
from database.database import Database


def init_database():
    """This function can be called to setup some of the few databases
    and collections."""

    # cvedb gets built by cve search

    # Download the relevant databases and insert them
    # Debian List Announcements (DLAs)
    # Create Collections
    db = Database()

    try:
        db.database.debian.create_collection("dla")
    except Exception as e:
        logger.info("Failed to create dsa collection: %s", e)

    try:
        db.database.debian.create_collection("dsa")
    except Exception as e:
        logger.info("Failed to create dla collection: %s", e)

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

    dlacollection = db.database.debian.get_collection("dla")
    dla_collector = DLACollector()
    dlas = dla_collector.get_d_as()
    for dla in dlas:
        # Index is created later
        dlacollection.insert(dla.to_dict())

    dsacollection = db.database.debian.get_collection("dsa")
    dsa_collector = DSACollector()
    dsas = dsa_collector.get_d_as()
    for dsa in dsas:
        # Index is created later
        dsacollection.insert(dsa.to_dict())

    pkg_collector = PackageCollector()
    pkg_collector.download_packages(pkg_collector.download_pkg_names())

    download_debian_security_tracker_json()

    insert_debian_package_name_aliases("./resources/debian_package_aliases.txt")


if __name__ == '__main__':
    start = datetime.now()
    init_database()
    end = datetime.now()
    logger.info("Data collection took %s", end - start)
