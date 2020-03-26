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
import database.database as database
import os
import unittest


class DBConfigTest(unittest.TestCase):
    def test_config(self):
        test_path = os.path.dirname(os.path.realpath(__file__)) + "/testcfg.json"

        # actual testing
        cfg = database.dbConfig.DBConfig(test_path)

        cfg.props.port = 123456
        cfg.save_config()

        # reload config
        cfg = database.dbConfig.DBConfig(test_path)

        self.assertEqual(cfg.props.port, 123456)

        os.remove(test_path)
