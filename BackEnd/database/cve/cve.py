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
This module contains methods for dealing with cves.
"""

from database import db


def get_cwe_by_ids(ids: list):
    """
    For a list of CWE ids this method returns a mapping from CWE id
    to CWE information.
    """
    filt = {"id": {"$in": ids}}
    proj = {"_id": 0}
    cwes = db.database.cvedb.cwe.find(filter=filt, projection=proj)
    cwes_dict = dict()

    for cwe in cwes:
        cwes_dict[cwe["id"]] = cwe

    return cwes_dict


def get_cves_by_ids(ids: list):
    """
    For a list of CVE ids this method returns a mapping from CVE id
    to CVE information.
    """
    filt = {"id": {"$in": ids}}
    proj = {"_id": 0}
    cves = db.database.cvedb.cves.find(filter=filt, projection=proj)
    cves_dict = dict()

    for cve in cves:
        cves_dict[cve["id"]] = cve

    return cves_dict


def get_cve_by_id(cve_id: str) -> dict:
    filt = {"id": cve_id}
    proj = {"_id": 0}
    return db.database.cvedb.cves.find_one(filter=filt, projection=proj)
