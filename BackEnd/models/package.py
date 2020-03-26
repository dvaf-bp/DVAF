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
from database import dbSerializable


class Package(dbSerializable.DBSerializable):
    def __init__(self, pkg_name="", description="", versions=None,
                 tags=None):
        super().__init__("pkg_name")
        self.db_pkg_name = pkg_name
        self.db_description = description
        self.db_tags = tags
        self.db_versions = versions

    @classmethod
    def from_dict(cls, dic):
        if dic is not None:
            try:
                dic["versions"] = [PackageVersion.from_dict(version)
                                   for version in dic.pop("versions", [])]
            except KeyError:
                dic["versions"] = {}
                dic["versions"] = [PackageVersion.from_dict(version)
                                   for version in dic.pop("versions", [])]
        else:
            dic = {"versions": {}}

        return cls(**dic)

    def to_dict(self):
        dic = dict()

        dic["pkg_name"] = self.db_pkg_name
        dic["description"] = self.db_description
        dic["tags"] = self.db_tags
        dic["versions"] = [version.to_dict() for version in self.db_versions]
        return dic


class PackageVersion(dbSerializable.DBSerializable):
    def __init__(self, pkg_name="", version="",
                 area="", suites=None, sloc=None):
        super().__init__("")
        self.db_pkg_name = pkg_name
        self.db_version = version
        self.db_area = area
        self.db_suites = suites
        self.db_sloc = sloc
        self.db_build_depends = None

    def set_dependencies(self, build_depends):
        self.db_build_depends = build_depends

    @classmethod
    def from_dict(cls, dic):
        build_depends = dic.pop('build_depends', None)
        version = cls(**dic)
        version.set_dependencies(build_depends)
        return version
