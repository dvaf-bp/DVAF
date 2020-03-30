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
This module compiles a report for a given package name.

group cves by time?

"apt": {
    "name": "apt",
    "description": "..."
    "use_tags": [...],

    # version specific
    "version": "...",
    "dependencies": [...],
    "sloc": {...}

    "aliases": ["abc", "def", ...],

    "open_cves": [<cve>, ...],
    "closed_cves": [<cve>, ...],
    "affecting_cves": [<cve>, ...],
    "open_cve_count": ...,
    "closed_cve_count": ...,
    "affecting_cve_count": ...,
    "dates":
}

"cve": {
    "id": ...,
    "published": ...,
    "cwe": ...,
    "summary": ...,
    "cvss": ...
}

"options": {
    "description": "no" / "yes",
    "use_tags": "no" / "yes",
    "version": "newest" / "123.567",
    "versions": "no" / "yes",
    "dependencies": "no" / "yes",
    "sloc": "no" / "yes",
    "aliases": "no" / "yes",
    "cves": "no" / "yes",
    "cve_report_options": dict,
    "group_cves": "no" / "day" / "month" / "year",
    "time_from": "DD-MM-YYYY",
    "time_to": "DD-MM-YYYY",
    "modified": "no" / "yes"
}
"""

from database import logger, db
from database.debian.version import deb_version_compare
from database.cve.cve_report import compile_cve_report
from database.util import get_default, daterange, parse_datetime
from datetime import datetime


def get_package_by_name(pkg_name):
    """
    """
    filt = {"pkg_name": pkg_name.lower()}
    return db.database.debian.packages.find_one(filter=filt)


def get_package_version(package, version_option):
    """
    """
    try:
        versions = package["versions"]

        if version_option == "newest":
            newest = versions[0]

            for ver in versions:
                cmp = deb_version_compare(ver["version"], newest["version"])

                if cmp > 0:
                    newest = ver

            return newest, versions
        else:
            for version in versions:
                if version["version"] == version_option:
                    return version, versions

            # no such version found
            return dict(), versions

    except KeyError as e:
        logger.fatal("Key error with the query " + str(e))
        return dict(), []


def get_dependencies(version: dict):
    """
    """
    return get_default(version, "dependencies", [])


def get_sloc(version: dict):
    """
    """
    return get_default(version, "sloc", [])


def get_aliases(pkg_name: str) -> list:
    """
    This method returns a list of all package aliases (all old/new names
    for that package).
    """
    filt1 = {"pkg_name": pkg_name}
    single = db.database.debian.package_aliases.find_one(filter=filt1)
    filt2 = {"aliases": {"$all": [pkg_name]}}
    entries = db.database.debian.package_aliases.find(filter=filt2)

    if single is None or entries is None:
        return []

    try:
        all_aliases = [] if single is None else single["aliases"]

        for e in entries:
            all_aliases += e["aliases"] + [e["pkg_name"]]

        alias_set = set(all_aliases)

        if pkg_name in alias_set:
            alias_set.remove(pkg_name)

        return list(alias_set)
    except KeyError as e:
        logger.fatal("KeyError for query " + pkg_name)
        return []


def does_affect(cve_id: str, pkg_version: str, release: dict):
    fixed_version = get_default(release, "fixed_version", None)

    if cve_id[0:3] != "CVE":
        return False

    cmp = 0

    # If the fixed version is newer than the current version
    # it is assumed to be unfixed.
    if fixed_version is not None:
        cmp = deb_version_compare(pkg_version, fixed_version)

    if fixed_version is None or cmp == -1:
        return True

    return False


def get_package_cves(pkg_name: str, pkg_version: str):
    filt = {"pkg_name": pkg_name}
    package = db.database.debian.package_to_cves.find_one(filter=filt)

    if package is None:
        return [], [], []

    open_cves = []
    closed_cves = []
    affecting_cves = []

    for cve in get_default(package, "cves", []):
        # no id, no release => don't make any assumptions
        if "cve_id" not in cve or "releases" not in cve:
            continue

        # check if in any release the cve is open, then it is
        # considered open
        any_open = False

        for release in ["stretch", "jessie", "sid",
                        "bullseye", "buster"]:
            # this cve does not exist in this release, skip
            if release not in cve["releases"]:
                continue

            # affecting cve
            if does_affect(cve["cve_id"], pkg_version,
                           cve["releases"][release]):
                affecting_cves.append(cve["cve_id"])

            # finally check status the safe way
            status = get_default(cve["releases"][release],
                                 "status",
                                 "closed")
            any_open |= status == "open"

        # append cve_id
        cve_id = cve["cve_id"]

        if any_open:
            open_cves.append(cve_id)
        else:
            closed_cves.append(cve_id)

    # done
    # eliminate duplicates
    open_cves = list(set(open_cves))
    closed_cves = list(set(closed_cves))
    affecting_cves = list(set(affecting_cves))

    return open_cves, closed_cves, affecting_cves


def group_cves_by_time(cves: list, dates: list) -> (list, list):
    """
    This method groups the cves by the published date.
    """
    # ["Jan 2018", "Feb 2018"], [[cves], [cves]]

    # sort cves by date
    cves.sort(key=lambda cve: cve["published"])
    # init, list of empty lists
    dict_cves = list()
    for _ in range(0, len(dates)):
        dict_cves.append(list())

    index = 0

    for cve in cves:
        published = cve["published"]

        while index < len(dates) - 1 and published >= dates[index + 1]:
            index += 1

        dict_cves[index].append(cve)

    return dict_cves


def filter_cves_date(cves: list, time_from: datetime,
                     time_to: datetime):
    """

    """
    filtered_cves = []

    for cve in cves:
        try:
            pub = cve["published"]

            if time_from <= pub and pub <= time_to:
                filtered_cves.append(cve)
        except KeyError as e:
            logger.fatal("cve has no key published")

    return filtered_cves


def compile_package_report(pkg_name: str, options: dict):
    description = ""
    use_tags = dict()
    dependencies = []
    sloc = None
    aliases = []
    open_cves = []
    closed_cves = []
    affecting_cves = []
    open_cve_count = 0
    closed_cve_count = 0
    affecting_cve_count = 0
    version_string = ""
    dates = []
    versions = []
    modified = ""

    package = get_package_by_name(pkg_name)

    if package is not None:
        if get_default(options, "description", "no") == "yes":
            description = get_default(package, "description", "")

        if get_default(options, "use_tags", "no") == "yes":
            use_tags = get_default(package, "tags", dict())

        version_option = get_default(options, "version", "newest")
        version, versions = get_package_version(package, version_option)

        if get_default(options, "version", "no") == "no":
            versions = []

        version_string = get_default(version, "version", "")

        if get_default(options, "dependencies", "no") == "yes":
            dependencies = get_dependencies(version)

        if get_default(options, "sloc", "no") == "yes":
            sloc = get_sloc(version)

        if get_default(options, "aliases", "no") == "yes":
            aliases = get_aliases(pkg_name)

        if get_default(options, "modified", "no") == "yes":
            modified = get_default(packages, "modified", "")

        if get_default(options, "cves", "no") == "yes":
            open_cves_ids, closed_cves_ids, affecting_cves_ids = \
                get_package_cves(pkg_name, version_string)

            cve_options = get_default(options, "cve_report_options",
                                      {"summary": "no",
                                       "published": "yes",
                                       "cwe": "yes",
                                       "cvss": "yes"})

            # init
            open_cves = []
            closed_cves = []
            affecting_cves = []

            for open_cve_id in open_cves_ids:
                entry = compile_cve_report(open_cve_id, cve_options)

                if entry is not None:
                    open_cves.append(entry)
                    open_cve_count = len(open_cves)

            for closed_cve_id in closed_cves_ids:
                entry = compile_cve_report(closed_cve_id, cve_options)

                if entry is not None:
                    closed_cves.append(entry)
                    closed_cve_count = len(closed_cves)

            for affecting_cve_id in affecting_cves_ids:
                entry = compile_cve_report(affecting_cve_id,
                                           cve_options)

                if entry is not None:
                    affecting_cves.append(entry)
                    affecting_cve_count = len(affecting_cves)

            # group by time
            group_by = get_default(options, "group_cves", "no")

            if group_by in ["day", "month", "year"]:
                time_from_str = get_default(options, "time_from", "")
                time_to_str = get_default(options, "time_to", "")
                time_from = parse_datetime(time_from_str)
                time_to = parse_datetime(time_to_str)
                dates = daterange(time_from, time_to, group_by)

                # only keep cves in time frame
                open_cves = filter_cves_date(open_cves, time_from,
                                             time_to)

                closed_cves = filter_cves_date(closed_cves, time_from,
                                               time_to)

                affecting_cves = filter_cves_date(affecting_cves,
                                                  time_from, time_to)

                open_cves = group_cves_by_time(open_cves, dates)
                closed_cves = group_cves_by_time(closed_cves, dates)
                affecting_cves = group_cves_by_time(affecting_cves,
                                                    dates)

                open_cve_count = []
                for cve_list in open_cves:
                    open_cve_count.append(len(cve_list))

                closed_cve_count = []
                for cve_list in closed_cves:
                    closed_cve_count.append(len(cve_list))

                affecting_cve_count = []
                for cve_list in affecting_cves:
                    affecting_cve_count.append(len(cve_list))

    return {
        "name": pkg_name,
        "description": description,
        "use_tags": use_tags,
        "version": version_string,
        "versions": versions,
        "dependencies": dependencies,
        "sloc": sloc,
        "aliases": aliases,
        "open_cves": open_cves,
        "open_cve_count": open_cve_count,
        "closed_cves": closed_cves,
        "closed_cve_count": closed_cve_count,
        "affecting_cves": affecting_cves,
        "affecting_cve_count": affecting_cve_count,
        "dates": dates,
        "modified": modified
    }


def compile_package_reports(pkg_names: list, options: dict,
                            pkg_versions: list = None) -> dict:
    """
    """
    result = dict()

    if pkg_versions is None:
        for pkg_name in pkg_names:
            report = compile_package_report(pkg_name, options)
            result[pkg_name] = report
    else:
        options_clone = options.copy()

        if len(pkg_names) != len(pkg_versions):
            return result

        for pkg_name, pkg_version in zip(pkg_names, pkg_versions):
            options_clone["version"] = pkg_version
            report = compile_package_report(pkg_name, options_clone)
            result[pkg_name] = report

    return result
