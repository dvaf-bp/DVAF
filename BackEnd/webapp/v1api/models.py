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
from webapp import app, db
from flask import jsonify
from datetime import datetime, timedelta


@app.route("/api/v1/dashboard", methods=['GET'])
def get_dashboard():
    cves = db.database.cvedb.cves

    time = datetime.now() - timedelta(days=1000)

    result = cves.aggregate([
        {
            "$match":
            {
                "Published":
                {
                    "$gte": time
                }
            }
        },
        {
            "$group":
            {
                "_id":
                {
                    "vector": "$access.vector", "cvss": "$cvss"
                },
                "count":
                {
                    "$sum": 1
                }
            }
        }
    ])

    proper = dict()

    # unpack, I'm not sure how to do this in mongo
    for entry in result:
        cvss = entry["_id"]["cvss"]
        vec = entry["_id"]["vector"] if "vector" in entry["_id"] else None
        count = entry["count"]

        if vec is not None:
            if vec not in proper:
                proper[vec] = dict()

            proper[vec][cvss] = count

            dlas = db.database.debian.dlas.find()
    dsas = db.database.debian.dsas.find()

    resp = {
        "cve_data": proper,
        "dsa_data": dlas.count(),
        "dla_data": dsas.count()
    }

    return jsonify(resp)


@app.route("/api/v1/stats/<string:distribution>/vulnerabilities", methods=[
    'GET'])
def get_vulnerabilities_by_distribution(distribution):
    # packages = db.find_objects("package", {"suites": distribution})
    return ""
