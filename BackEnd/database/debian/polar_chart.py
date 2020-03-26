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
from datetime import datetime


def get_max_cvss(report=None, time_from=datetime(year=1, month=1, day=1), time_to=datetime.now()):
    """
    This method returns the maximum cvss given a
    package report (see package_reprty.py).

    Args:
        report: The report.
        time_from: Only consider CVEs which got published after that date.
        time_to: Only consider CVEs which got published before that date.

    Returns:
        float: The highest cvss.
    """
    highest = 0

    for cve in report["open_cves"] + report["closed_cves"]:
        if time_from <= cve["published"] <= time_to:
            highest = max(highest, cve["cvss"])

    return highest


def get_avg_cvss(report=None, time_from=datetime(year=1, month=1, day=1), time_to=datetime.now()):
    """
    This method returns the average cvss given a
    package report (see package_reprty.py).

    Args:
        report: The report.
        time_from: Only consider CVEs which got published after that date.
        time_to: Only consider CVEs which got published before that date.

    Returns:
        float: The average cvss.
    """
    all_cves = report["open_cves"] + report["closed_cves"]
    count = 0
    cvss_sum = 0

    for cve in all_cves:
        if time_from <= cve["published"] and cve["published"] <= time_to:
            count += 1
            cvss_sum += cve["cvss"]

    if count == 0:
        return 0

    return cvss_sum / count


def create_polar_chart(package_reports=None, time_from=datetime(year=1, month=1, day=1), time_to=datetime.now()):
    """
    This method creates the data needed for the polar chart in the
    frontend.

    Args:
        package_reports: All the packages that should be accounted for.
        time_from: Only consider CVEs which got published after that date.
        time_to: Only consider CVEs which got published before that date.

    Returns:
        dict: All necessary information for the polar chart.
    """
    # sort by number of cves (all)
    reports = list(package_reports.items())
    reports.sort(key=lambda e: -(e[1]["open_cve_count"] + e[1]["closed_cve_count"]))

    chart = dict()
    total_cve_count = 0

    # top ten
    for report in reports[0:10]:
        pkg_name = report[0]
        entry = dict()

        cve_count = report[1]["open_cve_count"] + report[1]["closed_cve_count"]
        entry["cve_count"] = cve_count
        total_cve_count += cve_count

        max_cvss = get_max_cvss(report[1])
        entry["max_severity"] = max_cvss

        avg_cvss = get_avg_cvss(report[1])
        entry["avg_severity"] = avg_cvss

        chart[pkg_name] = entry

    # rest
    rest = reports[10:]

    # filter out all reports with 0 cves
    rest = [(name, report) for name, report in rest if report["open_cve_count"] and report["closed_cve_count"] > 0]

    chart_rest = dict()

    rest_cve_count = sum(map(lambda e: e[1]["open_cve_count"] + e[1]["closed_cve_count"], rest))
    if len(rest) > 0:
        chart_rest["cve_count"] = rest_cve_count / len(rest)
    else:
        chart_rest["cve_count"] = 0

    if len(rest) > 0:
        chart_rest["max_severity"] = sum(map(lambda e: get_max_cvss(e[1]), rest)) / len(rest)
        chart_rest["avg_severity"] = sum(map(lambda e: get_avg_cvss(e[1]), rest)) / len(rest)
    else:
        chart_rest["max_severity"] = 0
        chart_rest["avg_severity"] = 0

    total_cve_count += rest_cve_count
    chart["total_cve_count"] = total_cve_count

    chart["rest"] = chart_rest

    return chart
