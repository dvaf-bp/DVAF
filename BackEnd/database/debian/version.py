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
This module is for determining lexicographical order of debian package
version strings.
"""


def deb_version_extract(ver: str) -> list:
    """
    This function extract epoch, upstream-version and debian-revision
    from the verion string. The version string has the following format:
    [epoch:]upstream-version[debian-revision]
    """
    # regex does more harm than good in this case
    colon_index = ver.find(":")
    epoch = "0" if colon_index == -1 else ver[0:colon_index]

    minus_index = ver.rfind("-")
    revision = ""

    if minus_index != -1:
        revision = ver[minus_index:len(ver) - 1]

    version = ver[colon_index + 1:max(len(ver), minus_index)]

    return epoch, version, revision


def deb_extract_prefix(ver: str) -> (str, str):
    """
    This method extracts the prefix part of a version string which
    contains only digits or only non digists. In addition it returns
    the remainder of the version string after extraction.
    """
    if len(ver) == 0:
        return "", ""

    dig = str(ver[0]).isdigit()

    if dig:
        for i in range(0, len(ver)):
            if not ver[i].isdigit():
                return ver[0:i], ver[i:len(ver)]
    else:
        for i in range(0, len(ver)):  # noqa
            if ver[i].isdigit():
                return ver[0:i], ver[i:len(ver)]

    return ver, ""


def deb_ascii_compare(c1: str, c2: str):
    min_len = min(len(c1), len(c2))

    for i in range(0, min_len):
        # tilde is special case
        c1_tilde = c1[i] == "~"
        c2_tilde = c2[i] == "~"

        if c1_tilde and not c2_tilde:
            return -1
        elif not c1_tilde and c2_tilde:
            return 1

        if c1[i] < c2[i]:
            return -1
        elif c1[i] > c2[i]:
            return 1

    if len(c1) < len(c2):
        return -1
    elif len(c1) > len(c2):
        return 1
    else:
        return 0


def int_compare(i1: int, i2: int) -> int:
    if i1 > i2:
        return 1
    elif i1 == i2:
        return 0
    else:
        return -1


def deb_version_compare(v1: str, v2: str) -> int:
    """
    This function compares two debian package version strings.
    Everything will crash if v1 or v2 are not strings, take care.
    If v1 is less than v2 -1 is returned.
    If v1 is equal to v2 0 is returned.
    If v1 is larger than v2 1 is returned.
    See man deb-version for more information.
    """
    epoch1, version1, revision1 = deb_version_extract(v1)
    epoch2, version2, revision2 = deb_version_extract(v2)

    if epoch1 < epoch2:
        return -1
    elif epoch1 > epoch2:
        return 1

    # compare versions
    while version1 != "" or version2 != "":
        prefix1, version1 = deb_extract_prefix(version1)
        prefix2, version2 = deb_extract_prefix(version2)

        if prefix1.isdigit() and prefix2.isdigit():
            cmp = int_compare(int(prefix1), int(prefix2))
        else:
            cmp = deb_ascii_compare(prefix1, prefix2)

        if cmp != 0:
            return cmp

    # compare revisions
    while revision1 != "" or revision2 != "":
        prefix1, revision1 = deb_extract_prefix(revision1)
        prefix2, revision2 = deb_extract_prefix(revision2)

        if prefix1.isdigit() and prefix2.isdigit():
            cmp = int_compare(int(prefix1), int(prefix2))
        else:
            cmp = deb_ascii_compare(prefix1, prefix2)

        if cmp != 0:
            return cmp

    # equal
    return 0
