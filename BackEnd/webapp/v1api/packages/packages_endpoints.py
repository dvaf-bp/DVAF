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
This module provides all the endpoints for querying package information.
A lot of these endpoints return a **package report**. A
**package report** is a JSON containt all sorts of information about a
given package. The structure is as follows:
.. code-block::

    {
        "name": ...,
        "description": ...,
        "use_tags": ...,
        "version": ...,
        "versions": ...,
        "dependencies": ...,
        "sloc": ...,
        "aliases": ...,
        "open_cves": ...,
        "open_cve_count": ...,
        "closed_cves": ...,
        "closed_cve_count": ...,
        "affecting_cves": ...,
        "affecting_cve_count": ...,
        "dates": ...
    }

See **TODO** for more information.
"""

import re
from webapp import app
from flask import jsonify, request
from database.debian.packages import (
    parse_datetime,
    get_cve_count_by_time_freq
)
from database.cve.cve import (
    get_cwe_by_ids
)
from database.debian.package_report import (
    compile_package_report, compile_package_reports
)
from database.debian.browse_packages import (
    get_name_similar_packages,
    get_similar_packages_by_tags
)
from database.debian.polar_chart import (
    create_polar_chart
)


@app.route("/api/v1/packages/match/<string:name>", methods=["GET"])
def ep_match_packages(name):
    """
    This function takes an incomplete package name and returns a list
    of packages which have a similar name.

    Args:
        URL: */api/v1/packages/match/<string:name>*
        name: A (incomplete) package name for which this function
            shall return similar packages by name.

    Returns:
        str: A JSON string containing all packages with a similar name
            sorted by their similarity.

            .. code-block::

                [
                    {
                        "aliases": [],
                        "highest_affecting_cvss": 6.4,
                        "name": "firefox",
                        "version": "70.0.1-1",
                        ...
                    },
                    {
                        "aliases": [
                            "mozilla-firefox",
                            "mozilla$",
                            "iceweasel"
                        ],
                        "highest_affecting_cvss": 5.0,
                        "name": "firefox-esr",
                        "version": "68.2.0esr-1~deb10u1",
                        ...
                    },
                    ...
                ]
    """

    return jsonify(get_name_similar_packages(name, 20))


@app.route("/api/v1/packages/match/tags/<string:name>", methods=["GET"])
def ep_match_tags_packages(name):
    """
    This function takes an imcomplete package name and returns a list
    of packages which have a similar name.
    See get_similar_packages_by_tags() for more information.
    """

    return jsonify(get_similar_packages_by_tags(name, 20))


@app.route("/api/v1/packages/<string:name>", methods=['GET'])
def ep_get_package_by_name(name):
    """
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
            "description": "yes",
            "use_tags": "yes",
            "version": "newest",
            "dependencies": "yes",
            "sloc": "yes",
            "aliases": "yes"
        }

    Args:
        URL: */api/v1/packages/<string:name>*
        name: The precise package name.

    Returns:
        str: A JSON string of the **package report**.

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
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
            "description": "yes",
            "use_tags": "yes",
            "version": version,
            "dependencies": "yes",
            "sloc": "yes",
            "aliases": "yes"
        }

    Args:
        URL: */api/v1/packages/<string:name>/<string:version>*
        name: The precise package name.

    Returns:
        str: A JSON string of the **package report**.

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
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
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

    I.e. this method returns all open/closed/affecting CVEs for a given
    package in a given timespan and groups them by day, month or year.

    Args:
        URL: */api/v1/packages/cves/<string:pkg_name>/<string:time_from>
            /<string:time_to>/<string:freq>*
        pkg_name: The precise package name
        time_from: Lower time bound in format DD-MM-YYYY
        time_to: Upper time bound in format DD-MM-YYYY
        freq: Specifies by which time interval the CVEs are grouped. Can
            be "day", "month" or "year"

    Returns:
        str: A JSON string of the **package report**.

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


@app.route("/api/v1/packages/<string:pkg_name>/<string:version>/"
           "dependencies",
           methods=['GET'])
def ep_get_package_dependencies(pkg_name, version):
    """
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
            "version": version,
            "dependencies": "yes",
            "aliases": "yes"
        }

    I.e. this method returns the dependencies and alternate names for
    a given package.

    Args:
        URL: */api/v1/packages/<string:pkg_name>/<string:version>/
            dependencies*
        pkg_name: The precise package name
        version: Can be the exact version string or "newest"

    Returns:
        str: A JSON string of the **package report**.

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
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
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

    I.e. this method returns all open/closed/affecting CVEs for a list
    of package names. The list of package names must be in the request
    body and have the following format:

    .. code-block::

        {
            "packages": ["apt", "firefox-esr", ...]
        }

    In addition detailed information about every CWE id is returned.
    The return format is as follows:

    .. code-block::

        {
            "packages": ...,
            "cwes": ...
        }

    Parameters:
        URL: */api/v1/packages/cves/open_closed*

    Returns:
        str: A JSON string of the **package report**.

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
    This method returns **package reports** with the following options
    enabled:
    .. code-block::

        {
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

    The list of packages must be provided as a JSON in the request body
    in the following format:

    .. code-block::

        {
            "packages": [
                ...,
                "xorg/oldstable,now 1:7.7+19 amd64  [Installiert,automatisch]",
                ...
            ]
        }

    This is just the output of :code:`apt list --installed`.

    Parameters:
        URL: */api/v1/packages/upload*

    Returns:
        str: A JSON string of the **package report**.

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
            "published": "yes",
            "cvss": "yes"
        }
    }

    reports = compile_package_reports(pkg_names, options, pkg_versions)
    chart = create_polar_chart(reports)

    resp = {
        "packages": reports,
        "polar_chart": chart
    }

    return jsonify(resp)


@app.route("/api/v1/packages/cves/count/<string:pkg_name>/"
           "<string:time_from>/<string:time_to>/<string:freq>",
           methods=["GET"])
def ep_get_cve_count_by_package(pkg_name, time_from, time_to, freq):
    """
    This method returns a **package report** with the following options
    enabled:
    .. code-block::

        {
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

    Args:
        URL: */api/v1/packages/cves/count/<string:pkg_name>/
            <string:time_from>/<string:time_to>/<string:freq>*
        pkg_name: The precise package name
        time_from: Lower time bound in format DD-MM-YYYY
        time_to: Upper time bound in format DD-MM-YYYY
        freq: Specifies in what intervals that CVE counts are grouped.
            Can be "day", "month" or "year".

    Returns:
        str: A JSON string of the **package report**.

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
