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
from database.debian.packages import (  # noqa
    group_cves_by_time,
    daterange
)
from database import db


def get_cves_over_time(time_from, time_to, freq):
    filt = {"Published": {"$gte": time_from, "$lte": time_to}}
    proj = {"_id": 0, "id": 1, "Published": 1}
    cur_cves = db.database.cvedb.cves.find(filter=filt, projection=proj)
    dates = daterange(time_from, time_to, freq)

    # convert cursor to list
    cves = list(cur_cves)
    labels, grouped_cves = group_cves_by_time(cves, dates)

    return labels, grouped_cves


def get_cve_count_over_time(time_from, time_to, freq):
    labels, grouped_cves = get_cves_over_time(time_from, time_to, freq)
    return labels, [len(cves) for cves in grouped_cves]
