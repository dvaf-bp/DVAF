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
import json
from models import cve
from database import dbSerializable


class DBSerializableTest(unittest.TestCase):
    """A class which tests the correct functionality of
    DBSerializable and DBPatchFile
    """

    def test_patch(self):
        patch_file_path = "test_patch.json"
        patch_file_dict = {
            "CVE-1234-5678": {
                "cve_id": "CVE-9999-0000",
                "cvss_rating": 99.99,
                "oval": {
                    "package": "apt"
                }
            }
        }

        spec_dict = {
            "cve_id": "CVE-9999-0000",
            "cvss_rating": 99.99,
            "references": ["https://abc.xyz"],
            "oval": {
                "package": "apt",
                "version": None,
                "dsa_ids": [],
                "dla_ids": []
            }
        }

        file = open(patch_file_path, "w")
        file.write(json.dumps(patch_file_dict))
        file.close()

        cve.CVE.set_patch_file(patch_file_path)

        some_cve = cve.CVE("CVE-1234-5678", 3.14, ["https://abc.xyz"])
        some_cve.patch()

        self.assertEqual(some_cve.to_dict(), spec_dict)

    def test_serializable(self):
        oval1 = cve.OvalDebian("apt", 1.23, ["DSA-1234-5678"],
                               ["DLA-1234-5678"])
        cve1 = cve.CVE("CVE-1234-5678", 3.14, [], oval1)

        oval2 = cve.OvalDebian("apt", 0.23,
                               ["DSA-5678-9999", "DSA-1111-2222"],
                               ["DLA-0000-1111"])
        cve2 = cve.CVE("CVE-1010-2020", 4.14, [], oval2)

        dict1 = cve1.to_dict()
        dict2 = cve2.to_dict()

        spec_dict1 = {
            "cve_id": "CVE-1234-5678", "cvss_rating": 3.14,
            "references": [],
            "oval": {
                "package": "apt",
                "version": 1.23,
                "dsa_ids": ["DSA-1234-5678"],
                "dla_ids": ["DLA-1234-5678"]
            }
        }

        spec_dict2 = {
            "cve_id": "CVE-1010-2020",
            "cvss_rating": 4.14,
            "references": [],
            "oval": {
                "package": "apt",
                "version": 0.23,
                "dsa_ids": ["DSA-5678-9999", "DSA-1111-2222"],
                "dla_ids": ["DLA-0000-1111"]
            }
        }

        self.assertEqual(dict1, spec_dict1)
        self.assertEqual(dict2, spec_dict2)
