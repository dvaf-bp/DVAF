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
import requests
import json
from collectors import logger
from database import db
from datetime import datetime


URL = "https://security-tracker.debian.org/tracker/data/json"


def download_debian_security_tracker_json():
    # get json
    try:
        r = requests.get(URL)
    except Exception as e:
        logger.fatal("Request error: " + str(e))
        return

    try:
        js = json.loads(r.text)
    except Exception as e:
        logger.fatal("JSON parser error: " + str(e))
        return

    # put into database
    docs = list()

    for pkg_name, content in js.items():
        doc = dict()
        doc["pkg_name"] = pkg_name
        doc["cves"] = list()

        for cve_id, cve_content in content.items():
            cve_doc = dict()
            cve_doc["cve_id"] = cve_id
            # some keys don't exist, that's ok
            cve_doc["scope"] = cve_content.get("scope", None)
            cve_doc["debianbug"] = cve_content.get("debianbug", None)
            cve_doc["description"] = cve_content.get("description",
                                                     None)
            cve_doc["releases"] = cve_content["releases"]

            doc["cves"].append(cve_doc)

        # doc is done, append
        docs.append(doc)

    # an exception is thrown if a single write operation fails
    try:
        db.database.debian.package_to_cves.insert_many(docs,
                                                       ordered=False)
    except Exception as e:
        logger.info("some exception occured: " + str(e))

    logger.info("Download of debian security tracker json successful.")
    logger.info("You can find it in the collection"
                "debian.package_to_cves")

    # each entry:
    # { name: "", last_updated: ... }
    filt = {"name": "debian_security_tracker"}
    up = {"$set": {"db_name": "debian",
                   "collection_name": "package_to_cves",
                   "last_updated": datetime.now()}}
    db.database.meta.last_updated.update_one(filter=filt,
                                             update=up,
                                             upsert=True)
