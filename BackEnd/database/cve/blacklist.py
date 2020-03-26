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
from database import logger


class CVEBlackList:
    """
    This class just loads a text file containing a list of CVE ids
    which will be excluded from any CVE query.
    """
    def __init__(self, file_path):
        self.cves = set()

        try:
            file = open(file_path, "r")

            for line in file.readlines():
                if len(line) > 0:
                    self.cves.add(line)

            file.close()
        except Exception as e:
            logger.fatal("Could not open blacklist file: " + str(e))
            logger.info("Using empty blacklist.")

    def is_blacklisted(self, cve_id):
        """
        Returns if the given cve_id is blacklisted.
        """
        return cve_id in self.cves
