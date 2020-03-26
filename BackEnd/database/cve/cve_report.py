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





"CVE-1234-5678": {
    "id": ...,
    "published": ...,
    "cwe": ...,
    "summary": ...,
    "cvss": ...
}
"""

from database.util import get_default
from database.cve.cve import get_cve_by_id
from datetime import datetime
from database.cve import bl


def compile_cve_report(cve_id, options):
    published = None
    cwe = None
    summary = None
    cvss = None

    if bl.is_blacklisted(cve_id):
        return None

    cve = get_cve_by_id(cve_id)

    if cve is None:
        return None

    if cve is not None:
        if get_default(options, "published", "no") == "yes":
            published = get_default(cve, "Published",
                                    datetime(year=1990, month=1, day=1))

        if get_default(options, "cwe", "no") == "yes":
            cwe = get_default(cve, "cwe", "")

        if get_default(options, "summary", "no") == "yes":
            summary = get_default(cve, "summary", "")

        if get_default(options, "cvss", "no") == "yes":
            cvss = get_default(cve, "cvss", "")

    return {
        "id": cve_id,
        "published": published,
        "cwe": cwe,
        "summary": summary,
        "cvss": cvss
    }
