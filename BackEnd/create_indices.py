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
import pymongo

from database import db

db.database.debian.packages.create_index("pkg_name", unique=True)

# dsa indices
dsa_id_index = pymongo.IndexModel("dsa_id")
packages_index = pymongo.IndexModel("packages")
date_index = pymongo.IndexModel("date")
db.database.debian.dsas.create_indexes([dsa_id_index,
                                        packages_index,
                                        date_index])

# dla indices
dla_id_index = pymongo.IndexModel("dla_id")
packages_index = pymongo.IndexModel("packages")
date_index = pymongo.IndexModel("date")
db.database.debian.dlas.create_indexes([dla_id_index,
                                        packages_index,
                                        date_index])
