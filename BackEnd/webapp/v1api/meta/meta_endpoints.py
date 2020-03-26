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


@app.route("/api/v1/meta/last_updated")
def ep_get_last_update():
    proj = {"_id": 0}
    result = db.database.meta.last_updated.find(projection=proj)
    # build a dict:
    # db_name.collection_name -> { }
    dic = dict()

    for entry in result:
        db_name = entry["db_name"]
        collection_name = entry["collection_name"]

        if db_name not in dic:
            dic[db_name] = dict()

        dic[db_name][collection_name] = dict(entry)

    return jsonify(dic)
