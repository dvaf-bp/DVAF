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
import json
import sys
import unittest
import os

from collectors.DLACollector import DLACollector
from database.database import Database

'''
The DSA module contains the following functions:
- def get_d_as(self)
- def get_d_a_name_from_url(self, d_a_repo_path)
- def get_d_a_repo_paths_from_remote_repo(self):
- def get_d_a_from_data(self, d_a_data_file):
- def get_gitlab_path_tree_from_remote_repo(self, root_url, path):
- def get_data_from_url(self, url):
'''

from collectors.DSACollector import DSACollector


class D_ACollectorTest(unittest.TestCase):
    def test_get_one_dsa(self):
        dsa_4362_gold_standard = None
        with open("./tests/dsa-4362.json") as dump_file:
            dsa_4362_gold_standard = json.load(dump_file)
        dsa_collector = DSACollector()
        dsa_4362s = dsa_collector.get_d_as_from_paths(
            ["/english/security/2019/dsa-4362.data",
             "/english/security/2019/dsa-4362.wml"])

        self.assertEqual(len(dsa_4362s), 1)
        dsa_4362 = dsa_4362s[0]
        self.assert_against_gold_standard(dsa_4362,
                                          dsa_4362_gold_standard, "4362")
        return True

    def test_dla(self):
        dla_1624_gold_standard = None
        with open("./tests/dla-1624.json") as dump_file:
            dla_1624_gold_standard = json.load(dump_file)
        dla_collector = DLACollector()
        dla_1624s = dla_collector.get_d_as_from_paths(
            ["/english/lts/security/2019/dla-1624.data",
             "/english/lts/security/2019/dla-1624.wml"])

        self.assertEqual(len(dla_1624s), 1)
        dla_1624 = dla_1624s[0]
        self.assert_against_gold_standard(dla_1624, dla_1624_gold_standard,
                                          "1624")
        return True

    def assert_against_gold_standard(self, d_a, d_a_gold_standard, d_a_id):
        self.assertEqual(d_a.db_d_a_id,
                         d_a_id)
        self.assertEqual(d_a.db_packages,
                         d_a_gold_standard["packages"])
        self.assertEqual(d_a.db_date,
                         d_a_gold_standard["report_date"])
        self.assertEqual(d_a.db_is_vulnerable,
                         d_a_gold_standard["isvulnerable"])
        self.assertEqual(d_a.db_fixed, d_a_gold_standard["fixed"])
        self.assertEqual(d_a.db_secrefs,
                         d_a_gold_standard["secrefs"])
        self.assertEqual(d_a.db_description,
                         d_a_gold_standard["description"])
        self.assertEqual(d_a.db_sectags,
                         None)
        self.assertEqual(d_a.db_fixed_section,
                         d_a_gold_standard["fixed-section"])

    def test_get_d_as(self):
        if os.getenv("LONGTIME_UNITTEST") != 'true':
            return

        dsa_collector = DSACollector()
        dsas = dsa_collector.get_d_as()

        dla_collector = DLACollector()
        dlas = dla_collector.get_d_as()

        dsa_ids = [dsa.db_d_a_id for dsa in dsas]
        dla_ids = [dla.db_d_a_id for dla in dlas]

        # test whether ids are unambiguous
        self.assertEqual(len(dsa_ids), len(set(dsa_ids)))
        self.assertEqual(len(dla_ids), len(set(dla_ids)))

    def d_a_testing(self):
        if os.getenv("LONGTIME_UNITTEST") != 'true':
            print("Skipping long time unittest")
            return

        db = Database()

        dla_collector = DLACollector()
        dlas = dla_collector.get_d_as()

        for dla in dlas:
            db.insert_object("dla", dla)

        dsa_collector = DSACollector()
        dsas = dsa_collector.get_d_as()

        for dsa in dsas:
            db.insert_object("dsa", dsa)
        sys.exit(0)
