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
from database import logger
from database.stats.stats import (
    get_cve_count_over_time,
    get_cves_over_time
)
from database.dashboard.cache import DashboardCache
from datetime import datetime
from math import floor

dashboardCache = DashboardCache()


def update_dashboard_cache():
    """
    This method can be called every now and then to update the data
    cached for the dashboard.
    """
    # cache all stuff from 1970 up until now
    time_from = datetime(year=1970, month=1, day=1)
    time_to = datetime.now()

    logger.info("Beginning caching CVE counts " + str(time_from) + " to " + str(time_to))

    value = get_cve_count_over_time(time_from, time_to, "year")
    dashboardCache.update("get_cve_count_over_time_year", value)

    value = get_cve_count_over_time(time_from, time_to, "month")
    dashboardCache.update("get_cve_count_over_time_month", value)

    value = get_cve_count_over_time(time_from, time_to, "day")
    dashboardCache.update("get_cve_count_over_time_day", value)

    logger.info("Done")
    logger.info("Beginning caching CVEs " + str(time_from) + " to " + str(time_to))

    value = get_cves_over_time(time_from, time_to, "year")
    dashboardCache.update("get_cves_over_time_year", value)

    value = get_cves_over_time(time_from, time_to, "month")
    dashboardCache.update("get_cves_over_time_month", value)

    value = get_cves_over_time(time_from, time_to, "day")
    dashboardCache.update("get_cves_over_time_day", value)

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
        val = dashboardCache.get_value("get_cve_count_over_time_year")
    elif freq == "month":
        val = dashboardCache.get_value("get_cve_count_over_time_month")
    elif freq == "day":
        val = dashboardCache.get_value("get_cve_count_over_time_day")

    if val is None:
        return get_cve_count_over_time(time_from, time_to, freq)

    dates, cves = val

    begin_index = binary_index(dates, time_from, False)
    end_index = binary_index(dates, time_to, True)

    _dates = dates[begin_index:end_index + 1]
    _cves = cves[begin_index:end_index + 1]

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
        val = dashboardCache.get_value("get_cves_over_time_year")
    elif freq == "month":
        val = dashboardCache.get_value("get_cves_over_time_month")
    elif freq == "day":
        val = dashboardCache.get_value("get_cves_over_time_day")

    if val is None:
        return get_cves_over_time(time_from, time_to, freq)

    dates, cves = val

    begin_index = binary_index(dates, time_from, False)
    end_index = binary_index(dates, time_to, True)

    _dates = dates[begin_index:end_index + 1]
    _cves = cves[begin_index:end_index + 1]

    return _dates, _cves
