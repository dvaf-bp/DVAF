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
from collectors.D_ACollector import D_ACollector
from models.dsa import DSA


class DSACollector(D_ACollector):
    def __init__(self):
        super(DSACollector, self).__init__(
            "https://salsa.debian.org/api/v4/projects/27155/repository/tree/",
            "https://salsa.debian.org/webmaster-team/webwml/raw/master/",
            "english/security",
            "dsa-")

    def get_d_a_from_data(self, d_a_data_file):
        d_a_matches = self.data_pattern_matcher.findall(d_a_data_file)

        possible_tag_names = ["pagetitle", "packages", "report_date",
                              "isvulnerable", "fixed", "secrefs",
                              "description", "sectags", "fixed-section"]

        d_a_data = {}
        for match in d_a_matches:
            d_a_data[match[0]] = match[1]

        # default initialize tag fields
        for tag in possible_tag_names:
            if tag not in d_a_data:
                d_a_data[tag] = None

        return DSA(None,
                   d_a_data["packages"],
                   d_a_data["report_date"],
                   d_a_data["isvulnerable"],
                   d_a_data["fixed"],
                   d_a_data["secrefs"],
                   d_a_data["description"],
                   d_a_data["sectags"],
                   d_a_data["fixed-section"])
