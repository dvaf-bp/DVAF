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
import logging
import psycopg2


# udd database info
UDD_HOST = "udd-mirror.debian.net"  # noqa
UDD_DATABASE = "udd"  # noqa
UDD_USER = "udd-mirror"  # noqa
UDD_PASSWORD = "udd-mirror"  # noqa


class UDD:
    def __init__(self):
        # Setup logger
        path = './dvaf_backend.log'
        fmt = '%(asctime)-15s -[%(module)s, %(funcName)s]:\t%(message)s'
        logging.basicConfig(
            filename=path,
            format=fmt)
        self.logger = logging.getLogger('d_aCollector')

        try:
            self.conn = psycopg2.connect(host=UDD_HOST,
                                         database=UDD_DATABASE,
                                         user=UDD_USER,
                                         password=UDD_PASSWORD)
            self.cursor = self.conn.cursor()
            self.logger.info("UDD connection established.")
        except Exception as e:
            msg = "UDD connection could not be established: " + str(e)
            self.logger.fatal(msg)

    def close(self):
        self.cursor.close()
        self.conn.close()
