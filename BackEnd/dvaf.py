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
from webapp import app
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from collectors.download_schedule import download
from database.dashboard.dashboard import update_dashboard_cache


if __name__ == "__main__":
    # setup scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=download, trigger="interval",
                      seconds=60 * 60 * 24)
    scheduler.start()

    # kill scheduler on exit
    atexit.register(lambda: scheduler.shutdown())

    app.run()
