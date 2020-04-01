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

"""
This module contains the download schedule for all the data. It's run
every 24 hours.
"""
from datetime import datetime

from collectors import logger
from collectors.DLACollector import DLACollector
from collectors.DSACollector import DSACollector
from collectors.deb_sec_tracker import (
    download_debian_security_tracker_json
)
from collectors.cve_collector import (
    collect_cves
)
from collectors.debian_aliases import insert_debian_package_name_aliases
from collectors.pkg_data_collector import PackageCollector

from database import db

from database.dashboard.dashboard import update_dashboard_cache
from collectors.cwe_collector import collect_cwe_structure


def download():
    starttime = datetime.now()
    logger.info("Beginning download of all data.")

    # the file is only a few MB large, don't worry about timing out etc
    logger.info("Downloading CVEs")
    collect_cves()
    logger.info("Adding Package Aliases")
    insert_debian_package_name_aliases("./resources/debian_package_aliases.txt")
    logger.info("Collecting DLAs")

    try:
        dlacollection = db.database.debian.get_collection("dla")
        dla_collector = DLACollector()
        dlas = dla_collector.get_d_as()
        for dla in dlas:
            # Index is created later
            dlacollection.insert(dla.to_dict())
    except Exception as e:
        logger.error("Failed to download dlas: %s", e)

    logger.info("Collecting DSAs")

    try:
        dsacollection = db.database.debian.get_collection("dsa")
        dsa_collector = DSACollector()
        dsas = dsa_collector.get_d_as()
        for dsa in dsas:
            # Index is created later
            dsacollection.insert(dsa.to_dict())
    except Exception as e:
        logger.error("Failed to download dsas: %s", e)

    logger.info("Downloading packages")
    pkg_collector = PackageCollector()
    pkg_collector.download_packages(pkg_collector.download_pkg_names())

    logger.info("Downloading debian security tracker json.")
    download_debian_security_tracker_json()

    logger.info("Updating dashboard cache")
    update_dashboard_cache()

    logger.info("Downloading CWE structure tree.")
    try:
        collect_cwe_structure()
        logger.info("Done!")
    except Exception as e:
        logger.fatal("Something went wrong: " + str(e))

    logger.info("Finished update, took " + str(datetime.now() - starttime))
