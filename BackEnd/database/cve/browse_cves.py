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
from database import db
import re


def get_similar_cves_by_id(partial_id, limit=20):
    """
    This method returns all CVE's that have the partial_id in common.
    At most limit number if CVE's get returned.
    Args:
        partial_id: The CVE id.
        limit: Maximum number if CVE's that should be returned.

    Returns:
        list: A list of CVE's.
    """
    filt = {"id": {"$regex": re.compile(".*" + partial_id + ".*")}}
    proj = {"id": 1, "summary": 1, "cvss": 1, "_id": 0}
    results = db.database.cvedb.cves.find(filter=filt, projection=proj).limit(limit)
    return list(results)
