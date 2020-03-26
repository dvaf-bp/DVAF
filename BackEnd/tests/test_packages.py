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
import unittest

from models.package import Package, PackageVersion


class PackageTest(unittest.TestCase):
    def setUp(self):
        return

    def test_fromdict(self):
        package = Package().from_dict(None)
        self.assertEqual({}, package.db_versions)
        self.assertEqual("", package.db_pkg_name)

        package = Package().from_dict({"pkg_name": "testpackage"})
        self.assertEqual("testpackage", package.db_pkg_name)

    def test_packageversion_fromdict(self):
        dic = dict()
        dic['build_depends'] = {}

        pkgver = PackageVersion().from_dict(dic)
        self.assertEqual({}, pkgver.db_build_depends)
