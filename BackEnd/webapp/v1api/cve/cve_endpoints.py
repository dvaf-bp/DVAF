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
from flask import jsonify
from webapp import app
from flask import request
from database.cve.cve import get_cves_by_ids, get_cwe_by_ids


@app.route("/api/v1/cves/info", methods=["POST"])
def ep_get_cves_information():
    """
    This endpoint receives a list of CVE ids in the following form
    {
        "cves": ["CVE-1234-5678", "CVE-0000-1111", ...]
    }
    and returns all CVE and CWE information in the following form
    {
        "cves": {
            "CVE-1234-5678": {
                ...
            },
            "CVE-0000-1111": {
                ...
            },
            ...
        },
        "cwes": {
            "101": {
                ...
            },
            "403": {
                ...
            },
            ...
        }
    }
    """
    js = request.json
    cve_ids = js["cves"]

    cves = get_cves_by_ids(cve_ids)
    cwe_ids = set()

    for cve in cves.values():
        if "cwe" in cve:
            parts = cve["cwe"].split("-")

            if len(parts) <= 1:
                continue

            cwe_id = parts[1]
            # replace it with correct format
            cve["cwe"] = cwe_id
            cwe_ids.add(cwe_id)

    cwes = get_cwe_by_ids(list(cwe_ids))

    resp = {
        "cves": cves,
        "cwes": cwes
    }

    return jsonify(resp)
