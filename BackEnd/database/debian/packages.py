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
from database import db, logger
from datetime import datetime, timedelta
from database.debian.version import deb_version_compare


def get_dlas_dsas(pkg_pred) -> (list, list):  # noqa
    """
    This method returns all dlas and dsas associated with the given
    package predicate pkg_pred. Some example values for pkg_pred are
    "apt", {"$in": ["firefox-esr", "apt]}.
    """
    dlas = db.database.debian.dlas.find(filter={"packages": pkg_pred},
                                        projection={"_id": 0})
    dsas = db.database.debian.dsas.find(filter={"packages": pkg_pred},
                                        projection={"_id": 0})

    return list(dlas), list(dsas)


def get_secrefs(pkg_pred) -> list:
    """
    This method returns all secrefs associated with the given package
    predicate pkg_pred. Some example values for pkg_pred are
    "apt", {"$in": ["firefox-esr", "apt"]}.
    """
    dlas, dsas = get_dlas_dsas(pkg_pred)
    secrefs = []

    for d in dlas + dsas:
        if "secrefs" not in d or d["secrefs"] is None:
            continue

        parts = d["secrefs"].split(" ")
        secrefs += parts

    return secrefs


def get_cves(pkg_pred, time_from: datetime, time_to: datetime) -> list:
    """
    This method returns all cves that belong to the packages specified
    by pkg_pred and were published between time_from and time_to.
    Examples:
    get_cves("apt", datetime(1990, 1, 1), datetime(2000, 1, 1))
    get_cves({"$in": ["apt", "firefox-esr"]},
             datetime(1990, 1, 1), datetime(2000, 1, 1))
    """
    secrefs = get_secrefs(pkg_pred)

    cves = db.database.cvedb.cves.aggregate([
        {
            "$match": {
                "id": {
                    "$in": secrefs
                },
                "Published": {
                    "$gte": time_from,
                    "$lte": time_to
                }
            }
        },
        {
            "$project": {
                "_id": 1,
                "id": 1,
                "Published": 1,
                "summary": 1
            }
        }
    ])

    cleaned_cves = list()

    for cve in cves:
        cleaned_cve = cve
        cleaned_cve["_id"] = str(cleaned_cve["_id"])
        cleaned_cves.append(cleaned_cve)

    return cleaned_cves


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


def group_cves_by_time(cves: list, dates: list) -> (list, list):
    """
    This method groups the cves by the published date.
    """
    # ["Jan 2018", "Feb 2018"], [[cves], [cves]]

    # sort cves by date
    cves.sort(key=lambda cve: cve["Published"])
    # init, list of empty lists
    dict_cves = list()
    for _ in range(0, len(dates)):
        dict_cves.append(list())

    index = 0

    for cve in cves:
        published = cve["Published"]

        while index < len(dates) - 1 and published >= dates[index + 1]:
            index += 1

        dict_cves[index].append(cve)

    return dates, dict_cves


def get_cves_by_time_freq(pkg_pred, time_from: datetime,
                          time_to: datetime, freq: str) -> ([], []):
    """
    This method returns an array of datetimes (representing the time
    intervals) and an array containg the list of cves in that particular
    interval.
    """

    # invalid value for freq, return empty arrays
    if freq not in ["day", "month", "year"]:
        return [], []

    cves = get_cves(pkg_pred, time_from, time_to)
    rng = daterange(time_from, time_to, freq)

    return group_cves_by_time(cves, rng)


def get_cve_count_by_time_freq(pkg_pred, time_from: datetime,
                               time_to: datetime,
                               freq: str) -> (list, list):
    """
    This method does the same as get_cves_by_time_freq() but
    counts the cves.
    """

    dates, cves = get_cves_by_time_freq(pkg_pred, time_from, time_to,
                                        freq)
    cves = list(map(len, cves))

    return dates, cves


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


def get_package_by_name(name: str):
    """
    This function returns all package information.
    :return: Package, can be None.
    """
    return db.database.debian.packages.find_one(filter={
        "pkg_name": name}, projection={"_id": 0})


def tail_matches(cpe_version: str, pkg_name: str, pkg_version: list):
    # cut off *
    cpe_parts = list(filter(lambda part: part != "*",
                            cpe_version.split(":")))
    cpe_len = len(cpe_parts)
    pkg_len = len(pkg_version)

    eq = True

    # check version tail
    for i in range(0, pkg_len):
        if cpe_parts[cpe_len - 1 - i] != pkg_version[pkg_len - 1 - i]:
            eq = False

    # check software name
    eq &= cpe_parts[cpe_len - 1 - pkg_len] == pkg_name

    return eq


def get_cves_version(pkg_name: str, pkg_version: list):
    """
    This method returns all cves, dsas, dlas for which the current
    version is vulnerable. This method is still in an experimental
    state.
    """
    dsas, dlas = get_dlas_dsas(pkg_name)
    secrefs = get_secrefs(pkg_name)
    # all cves which are connected via dlas, dsas
    cves = db.database.cvedb.cves.aggregate([{
        "$match": {
            "id": {
                "$in": secrefs
            }
        }
    }
    ])

    vuln_cves = list()

    for cve in cves:
        if "vulnerable_product" not in cve:
            continue

        cpe_versions = cve["vulnerable_product"]
        is_vuln = False

        for cpe_ver in cpe_versions:
            is_vuln |= tail_matches(cpe_ver, pkg_name, pkg_version)

        if is_vuln:
            vuln_cves.append(cve)

    open_cves = dict()

    for vuln_cve in vuln_cves:
        cve_id = vuln_cve["id"]
        open_cves[cve_id] = dict()
        open_cves[cve_id]["cve"] = vuln_cve
        open_cves[cve_id]["dsas"] = dict()
        open_cves[cve_id]["dlas"] = dict()

        for dsa in dsas:
            if not dsa["secrefs"]:
                continue

            if cve_id in dsa["secrefs"]:
                open_cves[cve_id]["dsas"][dsa["d_a_id"]] = dsa

        for dla in dlas:
            if not dla["secrefs"]:
                continue

            if cve_id in dla["secrefs"]:
                open_cves[cve_id]["dlas"][dla["d_a_id"]] = dla

    return open_cves


def get_cve(cve_id: str):
    """
    This method returns the whole cve given the id.
    """
    cve = db.database.cvedb.cves.find_one(filter={"id": cve_id},
                                          projection={"_id": 0})
    return cve


def get_cwe_id(cve_id: str) -> str:
    """
    This method just returns the cwe id for a given cve id or None
    if it doesn't exist.
    """
    cve = db.database.cvedb.cves.find_one(filter={"id": cve_id},
                                          projection={"cwe": 1})

    # catches all possible exceptions at once
    try:
        parts = cve["cwe"].split("-")
        cwe_id = parts[1]
    except Exception as e:  # noqa
        return None

    cwe = db.database.cvedb.cwe.find_one(filter={"id": cwe_id})

    if cwe is None or "id" not in cwe:
        return None

    return cwe["id"]


def get_cves_open_closed(pkg_names: list) -> dict:
    """
    This method returns all open and closed cves for the given package
    names. The return format is as follows:
    {
        "apt": {
            "open_cves": [{"cve_id": "CVE-1234-5678", "cwe_id": "101",
                           "cvss": 1.2}],
            "closed_cves": [...]
        },
        "firefox-esr": {
            ...
        },
        ...
    }
    """
    filt = {"pkg_name": {"$in": pkg_names}}
    pkgs = db.database.debian.package_to_cves.find(filter=filt)

    deb_releases = ["stretch", "jessie", "sid", "bullseye", "buster"]
    result = dict()

    for pkg in pkgs:
        entry = dict()
        open_cves = []
        closed_cves = []

        # add cves
        for cve in pkg["cves"]:
            cve_id = cve["cve_id"]
            # is any version still affected by this CVE?
            any_open = False

            for rel in deb_releases:
                if rel not in cve["releases"]:
                    continue

                any_open |= cve["releases"][rel]["status"] == "open"

            cwe_id = get_cwe_id(cve_id)

            # get cvss
            c = get_cve(cve_id)
            cvss = 0

            if c is not None and "cvss" in c:
                cvss = c["cvss"]

            doc = {"cve_id": cve_id, "cwe_id": cwe_id, "cvss": cvss}

            # if so, it is considered open
            if any_open:
                open_cves.append(doc)
            else:
                closed_cves.append(doc)

        entry["open_cves"] = open_cves
        entry["closed_cves"] = closed_cves
        result[pkg["pkg_name"]] = entry

    return result


def get_affecting_cves(pkg_name: str, pkg_version: str):
    filt = {"pkg_name": pkg_name}
    pkg = db.database.debian.package_to_cves.find_one(filter=filt)

    if pkg is None:
        return []

    deb_releases = ["stretch", "jessie", "sid", "bullseye", "buster"]
    affecting_cves = []

    for cve in pkg["cves"]:
        cve_id = cve["cve_id"]

        for rel in deb_releases:
            if rel not in cve["releases"]:
                continue

            release = cve["releases"][rel]

            # maybe useful?
            # status = cve["status"]
            fixed_version = None

            if "fixed_version" in release:
                fixed_version = release["fixed_version"]

            # some cve ids are invalid such as TEMP-...
            # ignore them
            if cve_id[0:3] != "CVE":
                continue

            # for now allow to ignore version comparison
            if pkg_version == "*":
                affecting_cves.append(cve_id)
                continue

            cmp = 0

            # If the fixed version is newer than the current version
            # it is assumed to be unfixed.
            if fixed_version is not None:
                cmp = deb_version_compare(pkg_version, fixed_version)

            if fixed_version is None or cmp == -1:
                affecting_cves.append(cve_id)

    result = []
    affecting_cves = list(set(affecting_cves))

    for cve in affecting_cves:
        filt = {"id": cve}
        proj = {"Published": 1, "summary": 1}
        info = db.database.cvedb.cves.find_one(filter=filt,
                                               projection=proj)

        published = "unknown"
        if info is not None and "Published" in info:
            published = info["Published"]

        summary = "unknown"
        if info is not None and "summary" in info:
            summary = info["summary"]

        doc = {
            "cve_id": cve,
            "published": published,
            "summary": summary
        }

        result.append(doc)

    return result


def get_package_aliases(pkg_name: str) -> list:
    """
    This method returns a list of all package aliases (all old/new names
    for that package).
    """
    filt1 = {"pkg_name": pkg_name}
    single = db.database.debian.package_aliases.find_one(filter=filt1)
    filt2 = {"aliases": {"$all": [pkg_name]}}
    entries = db.database.debian.package_aliases.find(filter=filt2)

    all_aliases = [] if single is None else single["aliases"]

    for e in entries:
        all_aliases += e["aliases"] + [e["pkg_name"]]

    alias_set = set(all_aliases)

    if pkg_name in alias_set:
        alias_set.remove(pkg_name)

    return list(alias_set)


def get_current_package_version(pkg_name: str) -> str:
    filt = {"pkg_name": pkg_name.lower()}
    pkg = db.database.debian.packages.find_one(filter=filt)

    if pkg is None or "versions" not in pkg:
        return ""

    versions = pkg["versions"]
    max_version = versions[0]

    for ver in versions:
        if "version" not in ver:
            continue

        cmp = deb_version_compare(ver["version"],
                                  max_version["version"])

        if cmp > 0:
            max_version = ver

    return max_version["version"]


def get_package_highest_severity(pkg_name: str):
    filt = {"pkg_name": pkg_name}
    pkg = db.database.debian.package_to_cves.find_one(filter=filt)
    deb_releases = ["stretch", "jessie", "sid", "bullseye", "buster"]

    if pkg is None:
        return 0

    open_cves = []

    for cve in pkg["cves"]:
        cve_id = cve["cve_id"]
        # is any version still affected by this CVE?
        any_open = False

        for rel in deb_releases:
            if rel not in cve["releases"]:
                continue

            any_open |= cve["releases"][rel]["status"] == "open"

        # if so, it is considered open
        if any_open:
            open_cves.append(cve_id)

    cve_filt = {"id": {"$in": open_cves}}
    cves = db.database.cvedb.cves.find(filter=cve_filt)

    if cves.count() == 0:
        return 0

    max_cvss = max(map(lambda cve: cve["cvss"] if "cvss" in cve else 0, cves))

    return max_cvss
