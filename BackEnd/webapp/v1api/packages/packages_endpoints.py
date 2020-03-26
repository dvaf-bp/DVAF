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
import re
from webapp import app
from flask import jsonify, request
from database.debian.packages import (
    parse_datetime,
    get_cve_count_by_time_freq)
from database.cve.cve import (
    get_cwe_by_ids
)
from database.debian.package_report import (
    compile_package_report,
    compile_package_reports
)
from database.debian.browse_packages import (
    get_name_similar_packages
)


@app.route("/api/v1/packages/match/<string:name>", methods=["GET"])
def ep_match_packages(name):
    """
    This function takes an imcomplete package name and returns a list
    of packages which have a similar name.
    See get_name_similar_packages() for more information.
    """

    return jsonify(get_name_similar_packages(name, 20))


@app.route("/api/v1/packages/<string:name>", methods=['GET'])
def ep_get_package_by_name(name):
    """
    This function takes a package name and returns a full report.
    See compile_package_report() for more information.
    """
    options = {
        "description": "yes",
        "use_tags": "yes",
        "version": "newest",
        "dependencies": "yes",
        "sloc": "yes",
        "aliases": "yes"
    }

    return jsonify(compile_package_report(name, options))


@app.route("/api/v1/packages/<string:name>/<string:version>", methods=[
    'GET'])
def ep_get_package_by_name_version(name, version):
    """
    This function compiles a full report for the given package name and
    version. See compile_package_report() for more information.
    """
    options = {
        "description": "yes",
        "use_tags": "yes",
        "version": version,
        "dependencies": "yes",
        "sloc": "yes",
        "aliases": "yes"
    }

    return jsonify(compile_package_report(name, options))


@app.route("/api/v1/packages/cves/<string:pkg_name>/<string:time_from>/"
           "<string:time_to>/<string:freq>", methods=["GET"])
def ep_get_cves_by_package(pkg_name, time_from, time_to, freq):
    """
    This function compiles a report containing all the kinds of CVEs
    regarding that package. The CVEs are grouped by (day/month/year)
    and sorted by date. See compile_package_report() for more
    information.
    pkg_name: the package name
    time_from: only CVEs newer than this date are collected
    time_to: only CVEs older than this date are collected
    freq: can be "day"/"month"/"year"
    """
    options = {
        "version": "newest",
        "cves": "yes",
        "cve_report_options": {
            "id": "yes",
            "published": "yes",
            "summary": "yes"
        },
        "group_cves": freq,
        "time_from": time_from,
        "time_to": time_to
    }
    report = compile_package_report(pkg_name, options)
    report["affecting_cves"] = None

    return jsonify(report)


@app.route("/api/v1/packages/cves/count/<string:pkg_name>/<string:time_from>/"
           "<string:time_to>/<string:freq>", methods=["GET"])
def ep_get_cvecounts_by_package(pkg_name, time_from, time_to, freq):
    t_from = parse_datetime(time_from)
    t_to = parse_datetime(time_to)

    dates, cves = get_cve_count_by_time_freq(pkg_name, t_from, t_to, freq)

    resp = {
        "labels": dates,
        "cves_count": cves
    }

    return jsonify(resp)


@app.route("/api/v1/packages/<string:pkg_name>/<string:version>/"
           "dependencies",
           methods=['GET'])
def ep_get_package_dependencies(pkg_name, version):
    """
    This method returns a "package report" with only dependencies
    and aliases enables. The version can either be "newest" or a valid
    debian version string.
    The return format is as follows:
    {
        "name": "apt",
        "description": None
        "use_tags": None,
        "version": version,
        "dependencies": ["libc", ...],
        "sloc": None,
        "aliases": ["abc", "def", ...],
        "open_cves": None,
        "closed_cves": None,
        "affecting_cves": None,
        "dates": None
    }
    """

    options = {
        "version": version,
        "dependencies": "yes",
        "aliases": "yes"
    }
    report = compile_package_report(pkg_name, options)

    return jsonify(report)


@app.route("/api/v1/packages/cves/open_closed", methods=["POST"])
def ep_get_cves_open_closed():
    """
    This method returns all open and closed CVEs for the given packages.
    In addition the CWE ids are placed alongside the CVE ids.
    The package names must lie in the request body in the following
    form:
    {
        "packages": ["apt", "firefox-esr", ...]
    }
    The return value will have the following form:
    {
        "packages": {
            "apt": {
                "description": ...
                "open_cves": [...],
                "closed_cves": [...],
                "affecting_cves": [],
                ...,
                "highest_open_cvss": ...
            },
            ...
        },
        "cwes": {
            "101": {
                # cwe information
            },
            "102": {
                # cwe information
            },
            ...
        }
    }
    """
    pkg_names = request.json["packages"]
    options = {
        "description": "yes",
        "use_tags": "no",
        "version": "newest",
        "dependencies": "yes",
        "sloc": "yes",
        "aliases": "yes",
        "cves": "yes",
        "cve_report_options": {
            "id": "yes",
            "published": "no",
            "cwe": "yes",
            "summary": "yes",
            "cvss": "yes"
        }
    }
    reports = compile_package_reports(pkg_names, options)
    cwe_set = set()

    for report in reports.values():
        highest_open_cvss = 0

        for cve in report["open_cves"]:
            highest_open_cvss = max(highest_open_cvss, cve["cvss"])
            parts = cve["cwe"].split("-")

            if len(parts) == 2:
                cwe_set.add(parts[1])

        report["highest_open_cvss"] = highest_open_cvss

    resp = {
        "packages": reports,
        "cwes": get_cwe_by_ids(list(cwe_set))
    }

    return jsonify(resp)


@app.route("/api/v1/packages/upload", methods=["POST"])
def ep_upload_packages():
    """
    This endpoint receives a json in the request body containting a
    list of all packages for which cves are collected and returned.
    The json must have the following format:
    {
        "packages": [
            "aglfn/oldstable,oldstable,now 1.7-3 all  ...",
            "alsa-utils/oldstable,oldstable,now 1.1.3-1 amd64 ...",
            ...
        ]
    }
    The resulting json has the following format:
    "zip": {
      "affecting_cves": [
        {
          "cvss": null,
          "cwe": null,
          "id": "CVE-2004-1010",
          "published": "Tue, 01 Mar 2005 05:00:00 GMT",
          "summary": "..."
        },
        ...
      ],
      "name": "zip",
      "version": ""
    },
    """

    js = request.json
    ex = re.compile("(?P<pkg_name>([a-z, A-Z, 0-9, \\-, _])+)/" + "(?P<stable>[a-z, A-Z, \\,]+)\\s+" + "(?P<version1>\\S+)" + ".*")

    # first put all package names in an array
    pkg_names = []
    pkg_versions = []

    for pkg_str in js["packages"]:
        parts = ex.match(pkg_str)

        if not parts:
            continue

        pkg_name = parts.groupdict()["pkg_name"]
        pkg_version = parts.groupdict()["version1"]

        if len(pkg_name) == 0:
            continue

        pkg_names.append(pkg_name)
        pkg_versions.append(pkg_version)

    options = {
        "use_tags": "no",
        "version": "newest",
        "dependencies": "no",
        "sloc": "no",
        "aliases": "no",
        "cves": "yes",
        "cve_report_options": {
            "summary": "yes",
            "published": "yes"
        }
    }
    reports = compile_package_reports(pkg_names, options, pkg_versions)

    # little hack: Save bandwidth by not sending open_cves, closed_cves
    for report in reports.values():
        report["open_cves"] = None
        report["closed_cves"] = None

    resp = {
        "packages": reports
    }

    return jsonify(resp)


@app.route("/api/v1/packages/cves/count/<string:pkg_name>/"
           "<string:time_from>/<string:time_to>/<string:freq>",
           methods=["GET"])
def ep_get_cve_count_by_package(pkg_name, time_from, time_to, freq):
    """
    This function compiles a report containing all the kinds of CVEs
    regarding that package. The CVEs are grouped by (day/month/year)
    and sorted by date. See compile_package_report() for more
    information.
    pkg_name: the package name
    time_from: only CVEs newer than this date are collected
    time_to: only CVEs older than this date are collected
    freq: can be "day"/"month"/"year"
    """
    options = {
        "version": "newest",
        "cves": "yes",
        "cve_report_options": {
            "id": "yes",
            "published": "yes"
        },
        "group_cves": freq,
        "time_from": time_from,
        "time_to": time_to
    }
    report = compile_package_report(pkg_name, options)
    # dirty little hack
    report["affecting_cves"] = None
    report["open_cves"] = None
    report["closed_cves"] = None

    return jsonify(report)
