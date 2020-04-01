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
"""
This module provides the highlevel interface for the dashboard.
This includes methods for querying data and caching results.
"""
from database import logger, db
from database.stats.stats import (
    get_cve_count_over_time,
    get_cves_over_time
)
from datetime import datetime
from math import floor
from database.cache import Cache

cves_cache = Cache("DashboardCache", "dashboard_cves", True)
cves_count_cache = Cache("DashboardCache", "dashboard_cves_count", True)


def update_dashboard_cache():
    """
    This method can be called every now and then to update the data
    cached for the dashboard.
    """

    # drop collections on start
    for col in db.database.cache.list_collection_names():
        db.database.cache.drop_collection(col)

    # cache all stuff from 1970 up until now
    time_from = datetime(year=1970, month=1, day=1)
    time_to = datetime.now()

    logger.info("Beginning caching CVE counts " + str(time_from) + " to " + str(time_to))

    value = get_cve_count_over_time(time_from, time_to, "year")
    cves_count_cache.update(value, parameter="year")

    value = get_cve_count_over_time(time_from, time_to, "month")
    cves_count_cache.update(value, parameter="month")

    value = get_cve_count_over_time(time_from, time_to, "day")
    cves_count_cache.update(value, parameter="day")

    logger.info("Done")
    logger.info("Beginning caching CVEs " + str(time_from) + " to " + str(time_to))

    value = get_cves_over_time(time_from, time_to, "year")
    cves_cache.update(value, parameter="year")

    value = get_cves_over_time(time_from, time_to, "month")
    cves_cache.update(value, parameter="month")

    value = get_cves_over_time(time_from, time_to, "day")
    cves_cache.update(value, parameter="day")

    logger.info("Done")


def binary_index(ls, val, return_max=False):
    """
    This method returns the index where val would be inserted if ls
    is sorted. If return_max = True, the upper bound, otherwise the
    lower bound is returned.
    """
    lo = 0
    hi = len(ls) - 1
    mid = lo

    while lo < hi - 1:
        mid = floor((hi + lo) / 2)

        if val < ls[mid]:
            hi = mid
        elif val > ls[mid]:
            lo = mid
        else:
            return mid

    if return_max:
        return hi
    else:
        return lo


def get_cve_count_over_time_cached(time_from, time_to, freq):
    """
    This method returns the cached data for the endpoint
    ep_get_cve_count_over_time_count(). It returns a list of dates and
    a list of list of CVE counts.
    """
    # default value
    val = [], []

    if freq == "year":
        # val = dashboardCache.get_value("get_cve_count_over_time_year")
        val = cves_count_cache.get("year")
    elif freq == "month":
        # val = dashboardCache.get_value("get_cve_count_over_time_month")
        val = cves_count_cache.get("month")
    elif freq == "day":
        # val = dashboardCache.get_value("get_cve_count_over_time_day")
        val = cves_count_cache.get("day")

    if val is None:
        return get_cve_count_over_time(time_from, time_to, freq)

    dates, cves = val

    begin_index = binary_index(dates, time_from, False)
    end_index = binary_index(dates, time_to, True)

    _dates = dates[begin_index:end_index]
    _cves = cves[begin_index:end_index]

    return _dates, _cves


def get_cves_over_time_cached(time_from, time_to, freq):
    """
    This method returns the cached data for the endpoint
    ep_get_cves_over_time_count(). It returns a list of dates and
    a list of list of CVEs.
    """
    # default value
    val = [], []

    if freq == "year":
        # val = dashboardCache.get_value("get_cves_over_time_year")
        val = cves_cache.get("year")
    elif freq == "month":
        # val = dashboardCache.get_value("get_cves_over_time_month")
        val = cves_cache.get("month")
    elif freq == "day":
        # val = dashboardCache.get_value("get_cves_over_time_day")
        val = cves_cache.get("day")

    if val is None:
        return get_cves_over_time(time_from, time_to, freq)

    dates, cves = val

    begin_index = binary_index(dates, time_from, False)
    end_index = binary_index(dates, time_to, True)

    _dates = dates[begin_index:end_index]
    _cves = cves[begin_index:end_index]

    return _dates, _cves
