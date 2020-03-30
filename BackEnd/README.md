
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

# Debian Vulnerability Analyzer Framework Backend

--- 
### Continuous Integration

[![Build Status](https://travis-ci.com/mowirth/dvaf_backend.svg?token=aKfekXYkm4skpk55N4bG&branch=development)](https://travis-ci.com/mowirth/dvaf_backend)
[![Code Coverage](https://codecov.io/gh/mowirth/dvaf_backend/branch/development/graph/badge.svg?token=gKhxEeb36m)](https://codecov.io/gh/mowirth/dvaf_backend)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/88a731445df3450f96c0339fa4deb4e8)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mowirth/dvaf_backend&amp;utm_campaign=Badge_Grade)

## Installation

DVAF requires Python 3.6+ and an existing MongoDB installation. 

#### Dependencies

Dependencies can be installed using pip, for example with pip install -r requirements.txt. Additional dependencies may be required.

### cve-search

The cve-search database must be initialized, please visit [cve-search](https://github.com/cve-search/cve-search).

### Database

The database is generated every night - to create the indices please use the setup.py script. To keep the database up-to-date, run dvaf.py. 

### Webserver

The webserver can be started over the wsgi.py file. We recommend using Gunicorn or another production-ready webserver to host DVAF. 

### Systemd

We recommend using two different systemd services

Example Webserver Systemd (change the paths to your local installation accordingly): 

```
[Unit]
Description=Debian Vulnerability Analyzer Framework

[Install]
WantedBy=multi-user.target
[Service]
User=dvaf_backend
PermissionsStartOnly=true
Environment="PATH=/opt/dvaf_backend/venv/bin"
WorkingDirectory=/opt/dvaf_backend
ExecStart=/opt/dvaf_backend/venv/bin/gunicorn --bind 127.0.0.1:6000 --timeout 300 wsgi:app
TimeoutSec=600
Restart=on-failure
RuntimeDirectoryMode=755
```

We also recommend running a reverse proxy in front of the webserver. 

Example Collector Systemd

```
[Unit]
Description=Debian Vulnerability Analyzer Framework Data Collector

[Install]
WantedBy=multi-user.target
[Service]
User=dvaf_backend
PermissionsStartOnly=true
WorkingDirectory=/opt/dvaf_backend
ExecStart=/opt/dvaf_backend/venv/bin/python /opt/dvaf_backend/dvaf.py
TimeoutSec=600
Restart=on-failure
RuntimeDirectoryMode=755
```