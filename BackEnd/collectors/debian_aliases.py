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


def insert_debian_package_name_aliases(path: str):
    file = open(path, "r")

    if not file:
        return

    alias_dict = dict()

    for line in file.readlines():
        parts = line.split("->")

        if len(parts) != 2:
            continue

        old_name = parts[0].strip()
        new_name = parts[1].strip()

        if old_name in alias_dict:
            alias_dict[old_name].append(new_name)
        else:
            alias_dict[old_name] = [new_name]

        if new_name in alias_dict:
            alias_dict[new_name].append(old_name)
        else:
            alias_dict[new_name] = [old_name]

    for k, v in alias_dict.items():
        for vv in v:
            filt = {"pkg_name": k}
            res = db.database.debian.package_aliases \
                    .find_one(filter=filt)

            if res is None:
                # not in collection
                doc = {"pkg_name": k, "aliases": [vv]}
                db.database.debian.package_aliases.insert(doc)
            else:
                # append
                d = {"$addToSet": {"aliases": vv}}
                db.database.debian.package_aliases.update(spec=filt,
                                                          document=d)
