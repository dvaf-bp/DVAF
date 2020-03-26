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
from datetime import datetime, timedelta


class DashboardCache:
    def __init__(self):
        self.entries = dict()

    def update(self, entry_name, value):
        entry = (datetime.now(), value)
        self.entries[entry_name] = entry

    def get_age(self, entry_name):
        if entry_name not in self.entries:
            return timedelta(days=0)
        return self.entries[entry_name][0]

    def get_value(self, entry_name):
        entry = self.entries.get(entry_name, None)

        if entry is None:
            return None

        # entry is a tuple, first entry is last update date,
        # second entry is cached value
        return entry[1]
