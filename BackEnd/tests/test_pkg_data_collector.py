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
import requests
from collectors.pkg_data_collector import PackageCollector
from models.package import PackageVersion
from tests import logger
from datetime import datetime


class PkgDataCollectorTest(unittest.TestCase):
    def setUp(self):
        self.collector = PackageCollector()
        # little hack, so we don't have to download all packages
        self.collector.conn = requests.Session()

    def test_download_package_names(self):
        pkg_names = self.collector.download_pkg_names()
        for name in ["apt", "firefox-esr", "openssl"]:
            self.assertTrue(name in pkg_names)

    def test_download_pkg_description(self):
        desc = self.collector.download_pkg_description("openssl")
        self.assertEqual(desc, "Secure Sockets Layer toolkit - cryptographic utility")

    def test_download_versions_for_package(self):
        versions = [
            '0.9.8o-4squeeze23',
            '0.9.8o-4squeeze14',
            '0.9.8g-15+lenny16',
            '0.9.8c-4etch9',
            '0.9.8c-4etch3+m68k1',
            '0.9.7e-3sarge5',
            '0.9.6c-2.woody.7'
        ]

        resp = self.collector.download_versions_for_package("openssl")
        print(resp)

        for version in versions:
            self.assertTrue(version in resp)

    def test_download_version_information_for_package(self):
        resp = self.collector \
            .download_version_information_for_package("openssl",
                                                      "1.0.1k-3")
        sloc = {
            "ansic": 274094,
            "perl": 69104,
            "makefile": 13221,
            "asm": 9007,
            "cpp": 4367,
            "sh": 3416,
            "lisp": 24
        }
        spec = PackageVersion(pkg_name="openssl", version="1.0.1k-3",
                              area="main", suites=["jessie-kfreebsd"],
                              sloc=sloc)

        # PackageVersion doesn't support check for equality
        self.assertEqual(resp.db_pkg_name, spec.db_pkg_name)
        self.assertEqual(resp.db_version, spec.db_version)
        self.assertEqual(resp.db_area, spec.db_area)
        self.assertEqual(resp.db_suites, spec.db_suites)
        self.assertEqual(resp.db_sloc, spec.db_sloc)
        self.assertEqual(resp.db_build_depends, spec.db_build_depends)

    def test_tags(self):
        self.collector.load_tags()
        tags = self.collector.get_tags("openssl")
        spec = [
            "implemented-in::c",
            "interface::commandline",
            "protocol::ssl",
            "role::program",
            "scope::utility",
            "security::cryptography",
            "security::integrity",
            "use::checking"
        ]
        logger.info(tags)
        self.assertEqual(tags, spec)

    def test_load_dependencies(self):
        self.collector.load_dependencies()
        self.assertIsNotNone(self.collector.dep_data)

    def test_load_package_data(self):
        self.collector.load_packagedata()
        self.assertIsNotNone(self.collector.pkg_data)

    def test_update_dependencies(self):
        pkg_info = self.collector.download_version_information_for_package("openssl", "1.0.1t-1+deb8u8")
        pkg_info2 = pkg_info
        self.collector.update_dependencies(pkg_info2)
        # TODO: Finish test

    def test_download_packages(self):
        self.collector.download_packages(['openssl', 'nginx'])
        # TODO: Finish test

    def test_upsert(self):
        pkg_names = ["firefox-esr"]
        filt = {"pkg_name": "firefox-esr"}

        self.collector.download_packages(pkg_names)
        before = self.collector.db.database.debian.packages.find_one(filter=filt)
        before["_id"] = 0
        before["modified"] = datetime(year=2000, month=1, day=1)

        self.collector.db.database.debian.packages.delete_one(filter=filt)

        self.collector.download_packages(pkg_names)
        after = self.collector.db.database.debian.packages.find_one(filter=filt)
        after["_id"] = 0
        after["modified"] = datetime(year=2000, month=1, day=1)

        self.assertEquals(before, after)
