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


class OvalDebian(dbSerializable.DBSerializable):
    def __init__(self, package=None, version=None, dsa_ids=[], dla_ids=[]):
        super().__init__("")
        self.db_package = package
        self.db_version = version
        self.db_dsa_ids = dsa_ids
        self.db_dla_ids = dla_ids


class CVE(dbSerializable.DBSerializable):
    def __init__(self, cve_id=None, cvss_rating=0, references=[],
                 oval=OvalDebian()):
        super().__init__("cve_id")
        self.db_cve_id = cve_id
        self.db_cvss_rating = cvss_rating
        self.db_references = references
        self.db_oval = oval

    @classmethod
    def from_dict(cls, dic):
        # For now arbitrary recursion depth is not supported!
        dic["oval"] = OvalDebian.from_dict(dic["oval"])
        return cls(**dic)

    def patch_attribute(self, name, value):
        new_value = OvalDebian.from_dict(value) if name == "oval" else value
        super().patch_attribute(name, new_value)
