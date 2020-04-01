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
import os

from database import db, logger
from datetime import datetime


def collect_cves():
    logger.info("Starting to collect CVEs")

    # run cve script
    os.system('python cvecollector/sbin/db_updater.py')

    logger.info("Collecting CVEs done.")

    filt = {"name": "cves"}
    up = {"$set": {"db_name": "cvedb",
                   "collection_name": "cves",
                   "last_updated": datetime.now()}}
    db.database.meta.last_updated.update_one(filter=filt,
                                             update=up,
                                             upsert=True)
