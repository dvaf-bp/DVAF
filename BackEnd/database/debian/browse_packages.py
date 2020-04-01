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
This module provides methods for searching for similar packages
by name and tags.
"""

import re
from database import db
from database.debian.levenshtein import levenshtein
from database.debian.package_report import (
    compile_package_reports,
    compile_package_report
)


def get_name_similar_packages(pkg_name, limit):
    """
    This function takes the an incomplete package name such as
    "fire" (when searching for "firefox") and returns a list of at most
    limit number of packages sorted by the similarity of the name.
    For example pkg_name="firefox", limit=20 yields:
    [
        {
            "aliases": [],
            "highest_affecting_cvss": 6.4,
            "name": "firefox",
            "version": "70.0.1-1",
            ...
        },
        {
            "aliases": [
                "mozilla-firefox",
                "mozilla$",
                "iceweasel"
            ],
            "highest_affecting_cvss": 5.0,
            "name": "firefox-esr",
            "version": "68.2.0esr-1~deb10u1",
            ...
        },
        ...
    ]
    """

    ex = re.compile(".*" + pkg_name.lower() + ".*")
    filt = {"pkg_name": {"$regex": ex}}
    proj = {"_id": 0, "pkg_name": 1}
    packages = db.database.debian.packages.find(filter=filt,
                                                projection=proj)
    pkg_names = list(map(lambda e: e["pkg_name"], packages))
    pkg_names.sort(key=lambda name: levenshtein(name, pkg_name))
    # Remove packages that exceed the limit
    pkg_names = pkg_names[0:limit]

    options = {
        "aliases": "yes",
        "cves": "yes",
        "description": "yes",
        "cve_report_options": {
            "cvss": "yes"
        }
    }

    reports = compile_package_reports(pkg_names, options)

    # Come hewe maximum sevewity, good boi OwO
    # Sowwy cves, you mwust go QwQ
    for report in reports.values():
        highest_affecting_cvss = 0

        if len(report["affecting_cves"]) > 0:
            highest_affecting_cvss = max(map(lambda e: e["cvss"],
                                             report["affecting_cves"]))
        report["highest_affecting_cvss"] = highest_affecting_cvss
        report["open_cves"] = None
        report["closed_cves"] = None
        report["affecting_cves"] = None

    reports = list(reports.values())
    reports.sort(key=lambda report: levenshtein(report["name"],
                                                pkg_name))

    return reports


def get_similar_packages_by_tags(pkg_name, lim):
    filt = {"pkg_name": pkg_name}
    proj = {"_id": 1, "pkg_name": 1, "tags": 1}
    pkg = db.database.debian.packages.find_one(filter=filt, projection=proj)

    result = db.database.debian.packages.aggregate([
        {
            "$project": {
                "pkg_name": "$pkg_name",
                "common_tag_count": {
                    "$size": {
                        "$setIntersection": ["$tags", pkg["tags"]]
                    }
                }
            }
        },
        {
            "$sort": {
                "common_tag_count": -1
            }
        }
    ])

    pkg_names = [r["pkg_name"] for r in result][0:lim]

    options = {
        "aliases": "yes",
        "description": "yes"
    }

    reports = []

    for pkg_name in pkg_names:
        report = compile_package_report(pkg_name, options)
        reports.append(report)

    return reports
