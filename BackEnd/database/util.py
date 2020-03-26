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
from database import logger


def get_default(dic, key_name, default_value):
    """

    """
    if key_name not in dic:
        return default_value

    val = dic[key_name]
    return val


def daterange(date_from: datetime, date_to: datetime, freq: str) -> []:
    """
    Creates an array of datetime for every date between date_from and
    date_to where the distance between two dates is specified by freq.
    freq can have the following values: "day", "month", "year"
    """
    rng = []

    if freq == "day":
        date_from = datetime(date_from.year, date_from.month,
                             date_from.day)
        date_to = datetime(date_to.year, date_to.month, date_to.day)
        date_curr = date_from

        while date_curr <= date_to:
            rng.append(date_curr)
            date_curr = date_curr + timedelta(days=1)
    elif freq == "month":
        # round dates down to month
        date_from = datetime(date_from.year, date_from.month, 1)
        date_to = datetime(date_to.year, date_to.month, 1)
        date_curr = date_from

        while date_curr <= date_to:
            rng.append(date_curr)

            # increase in month steps, rewind month
            if date_curr.month >= 12:
                date_curr = datetime(date_curr.year + 1, 1, 1)
            else:
                date_curr = datetime(date_curr.year,
                                     date_curr.month + 1, 1)
    elif freq == "year":
        # round dates down to year
        date_from = datetime(date_from.year, 1, 1)
        date_to = datetime(date_to.year, 1, 1)
        date_curr = date_from

        while date_curr <= date_to:
            rng.append(date_curr)
            date_curr = datetime(date_curr.year + 1, 1, 1)

    return rng


def parse_datetime(text) -> datetime:
    """
    This method parses the text and returns a datetime.
    The text has to have the format DD-MM-YYYY.
    The numbers have to be zero padded.
    """
    try:
        return datetime.strptime(text, "%d-%m-%Y")
    except ValueError as e:
        logger.info("received invalid date string: " + str(e))
        return datetime.now()
