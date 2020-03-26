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
from database import dbSerializable


class DSA(dbSerializable.DBSerializable):
    def __init__(self, d_a_id=None, packages=None, date=None,
                 is_vulnerable=None, fixed=None, secrefs=None,
                 description=None, sectags=None, fixed_section=None):
        super().__init__("d_a_id")
        # IDs
        self.db_d_a_id = d_a_id

        # Specifics
        self.db_packages = packages
        self.db_date = date
        self.db_is_vulnerable = is_vulnerable
        self.db_fixed = fixed
        self.db_secrefs = secrefs
        self.db_description = description
        self.db_sectags = sectags
        self.db_fixed_section = fixed_section
        # todo: self.db_pagetitle = pagetitle
