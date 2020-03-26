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
from database import database
from models import cve
import unittest


class DBConfigTest(unittest.TestCase):
    def test_init(self):
        database.init_database()
        self.assertTrue(True)

    def test_insert_object(self):
        db = database.Database()
        c = cve.CVE("CVE-1234-5678", 3.5, [], cve.OvalDebian())
        db.insert_object("testcves", c)
        result = db.database.admin.testcves.find_one(
            {"cve_id": "CVE-1234-5678"})
        result.pop("_id")
        self.assertEqual(c.to_dict(), cve.CVE.from_dict(result).to_dict())
