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
import flask
from webapp.config import Config
from database.database import Database
from flask_cors import CORS
import logging

app = flask.Flask(__name__)
CORS(app)
db = Database()
app.config.from_object(Config)

# setup per package logging
logger = logging.getLogger(__package__)
logger.propagate = False

# this can later be set in a config file
FORMAT = "%(asctime)-15s -[%(module)s, %(funcName)s]:\t%(message)s"
LOG_FILE_PATH = "./dvaf_backend.log"

# formatting
fh = logging.FileHandler(LOG_FILE_PATH)
fh.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(fh)

logger.setLevel(logging.INFO)
logger.info("Webapp logs will be saved in: " + LOG_FILE_PATH)

# This import must be located here, since it depends on the app and
# db vars
# importing this at the top would lead to cycling imports, so
# style checking
# is disabled for this line.
from webapp.v1api import models  # noqa
from webapp.v1api.packages import packages_endpoints  # noqa
from webapp.v1api.dashboard import dashboard_endpoints  # noqa
from webapp.v1api.cve import cve_endpoints  # noqa
