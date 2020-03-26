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
"""This module collects information about debian packages."""
import time
import logging
import requests
import psycopg2
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime

from database import Database
from models.package import Package
from models.package import PackageVersion

logging.basicConfig(
    filename='./dvaf_backend.log',
    format=' %(asctime)-15s -[%(module)s, %(funcName)s]:\t%(message)s')
logger = logging.getLogger('pkg_data_collector')

PKG_LIST_PATH = "https://sources.debian.org/api/list/"
PKG_VERSIONS_PATH = "https://sources.debian.org/api/src/{}/"
PKG_INFORMATION_PATH = "https://sources.debian.org/api/info/package/{}/{}/"
PKG_TRACKER_PATH = "https://tracker.debian.org/pkg/{}"
PKG_DEPENDENCIES_PATH = "https://packages.debian.org/{}/{}"
PKG_COLLECTION_NAME = "packages"


class PackageCollector:
    def __init__(self):
        self.conn = None
        self.bin2src = dict()
        self.tag_data = dict()
        self.db = Database()
        self.dep_data = dict()
        self.pkg_data = dict()

    def upsert_package(self, pkg_dict):
        dict_copy = pkg_dict.copy()
        dict_copy["modified"] = datetime.now()
        filt = {"pkg_name": dict_copy["pkg_name"]}
        up = {"$set": dict_copy}
        r = self.db.database.debian.packages.update_one(filter=filt,
                                                        update=up,
                                                        upsert=True)

    def done(self):
        # each entry:
        # { name: "", last_updated: ... }
        filt = {"name": "debian_packages"}
        up = {"$set": {"db_name": "debian",
                       "collection_name": "packages",
                       "last_updated": datetime.now()}}
        self.db.database.meta.last_updated.update_one(filter=filt,
                                                      update=up,
                                                      upsert=True)

    def download_packages(self, pkg_names):
        if self.conn is None:
            self.conn = requests.Session()

        self.load_tags()
        self.load_dependencies()
        self.load_packagedata()

        if pkg_names is not None:
            for p in tqdm(pkg_names, unit="Packages", desc="Downloading Debian Packages"):
                pkg = Package()
                pkg.db_pkg_name = p
                pkg.db_versions = []

                try:
                    pkg_desc = self.download_pkg_description(p)
                except Exception as e:
                    logger.error("Failed to download package description: %s", e)
                    pkg_desc = ""

                pkg.db_description = pkg_desc

                try:
                    pkg_versions = self.download_versions_for_package(p)
                except Exception as e:
                    logger.error("Failed to download packages for %s: %s", p, e)
                    pkg_versions = None

                if pkg_versions is not None:
                    for pv in pkg_versions:
                        try:
                            pkg_info = self.download_version_information_for_package(p, pv)
                        except Exception as e:
                            logger.error("Failed to download package information: %s", e)
                            pkg_info = None

                        if pkg_info is not None:
                            try:
                                self.update_dependencies(pkg_info)
                            except Exception as e:
                                logger.error("Failed to get dependencies: %s", e)
                        pkg.db_versions.append(pkg_info)

                try:
                    tags = self.get_tags(p)
                    pkg.db_tags = tags
                except Exception as e:
                    logger.error("Failed to get tags: %s", e)

                try:
                    # self.db.database.debian.packages.insert(pkg.to_dict())
                    self.upsert_package(pkg.to_dict())
                except Exception as e:
                    logger.error("Failed to insert package %s into database %s", p, e)

        self.done()

    def download_pkg_names(self):
        """
        Return a list containing the names of all debian packages.
        """
        response = self.request(PKG_LIST_PATH).json()
        pkgs = []
        if response is not None:
            try:
                for pkg in response["packages"]:
                    try:
                        pkgs.append(pkg["name"])
                    except KeyError:
                        pass
            except KeyError:
                pass

        return pkgs

    def download_pkg_description(self, pkg_name):
        """
        Return the description of the given package.
        """
        try:
            response = self.request(PKG_TRACKER_PATH.format(pkg_name)).content
        except Exception as e:
            logger.error("Failed to download package description: %s", e)
            return ""

        soup = BeautifulSoup(response, 'html.parser')
        desc = soup.find('h5')
        if desc is not None:
            return desc.text

        return ""

    def download_versions_for_package(self, pkg_name):
        """
        Return a list containing all versions of a given debian package.
        """
        versions = []
        try:
            response = self.request(PKG_VERSIONS_PATH.format(pkg_name))
        except requests.exceptions.HTTPError as e:
            logger.error("Failed to download package versions: %s", e)
            return versions

        if response is not None:
            try:
                response = response.json()
            except Exception as e:
                logger.error("Failed to parse response into json: %s", e)
                return None

            try:
                for version in response["versions"]:
                    try:
                        versions.append(version["version"])
                    except KeyError:
                        pass
            except KeyError:
                pass

        return versions

    def download_version_information_for_package(self, pkg_name, version):
        """
        Return a PackageVersion for the given version of a debian package.
        """
        try:
            response = self.request(PKG_INFORMATION_PATH.format(pkg_name, version))
        except Exception as e:
            logger.error("Failed to download package version: %s", e)
            return None

        if response is not None:
            try:
                response = response.json()
            except Exception as e:
                logger.error("Failed to parse response into json: %s", e)
                return None

            pkg_info = dict()
            area = []
            suites = []
            sloc = dict()
            try:
                pkg_info = response["pkg_infos"]
            except KeyError:
                pass

            try:
                area = pkg_info["area"]
            except KeyError:
                pass

            try:
                suites = pkg_info["suites"]
            except KeyError:
                pass

            if pkg_info is not None:
                try:
                    sloc = dict(pkg_info["sloc"])
                except KeyError:
                    pass

            version = PackageVersion(pkg_name, version, area, suites, sloc)
            return version

    def load_dependencies(self):
        cursor = psycopg2.connect(
            host="udd-mirror.debian.net",
            port=5432,
            database="udd",
            user="udd-mirror",
            password="udd-mirror").cursor()

        cursor.execute("SELECT source, version, release, build_depends FROM sources")
        res = cursor.fetchall()
        self.dep_data = {}
        for r in tqdm(res, unit="dependencies", desc="Loading dependencies"):
            name = r[0]
            version = r[1]
            dependencies = r[3:]
            index = "{}/{}".format(name, version)
            self.dep_data[index] = dependencies

    def load_packagedata(self):
        cursor = psycopg2.connect(
            host="udd-mirror.debian.net",
            port=5432,
            database="udd",
            user="udd-mirror",
            password="udd-mirror").cursor()

        cursor.execute("SELECT package, source, count(*) FROM packages GROUP BY package, source")
        self.pkg_data = {}
        res = cursor.fetchall()
        for r in tqdm(res, unit="pkgs", desc="Loading packages"):
            name = r[0]
            self.pkg_data[name] = r

        cursor.close()

    def update_dependencies(self, version):
        """
        collect the dependencies for the given version
        and update the information inside the PackageVersion Object
        """
        try:
            build_depends = self.dep_data["{}/{}".format(version.db_pkg_name, version.db_version)]
        except KeyError:
            return

        if build_depends is not None:
            if build_depends[0] is None:
                return

            deps = []
            for dep in build_depends[0].split(","):
                name = dep.strip().split(" ")[0]
                if name not in self.bin2src:
                    try:
                        data = self.pkg_data[name]
                    except KeyError:
                        continue
                    # sometimes there's more than 1 src package
                    # for now we choose the name which occurs more often
                    src = data

                    self.bin2src[name] = src[1]
                deps += [self.bin2src[name]]
            version.set_dependencies(deps)

    def request(self, url):
        """Return the content of the given url"""
        if self.conn is None:
            self.conn = requests.Session()
        download_failure_retries = 0
        while download_failure_retries < 30:
            # For stability, when an error occurs it is retried
            # to download and logged when the error persists
            try:
                return self.conn.get(url)
            except requests.Timeout:
                download_failure_retries += 1
                time.sleep(2)

            except requests.exceptions.HTTPError as errh:
                logger.error("HTTP Error: %s", errh)
            except requests.ConnectionError as e:
                logger.error("Failed to connect: %s", e)
            except requests.TooManyRedirects:
                logger.critical("BAD URL: '%s could not get any Data", url)
                return None
            except requests.RequestException as ex:
                download_failure_retries += 1
                time.sleep(2)
                logger.critical("URL '%s request could not be completed due to: %s", url, ex)

        logger.critical("URL '%s' request could not be completed due to too many retries", url)
        return None

    def load_tags(self):
        """
        download all the tag data and save them so the individual package can get them...
        """
        # tags downloaded via https://debtags.debian.org/exports/
        try:
            tag_data = requests.get("https://debtags.debian.org/exports/stable-tags").text
        except Exception as e:
            logger.error("Failed to download debian tag data: %s", e)
            return

        for pkg in tqdm(tag_data.splitlines(), unit="tags", desc="Splitting tags"):
            arr = pkg.split(": ")
            try:
                # arr[0] is the package name... the rest of the array contains the other tags?
                if len(arr) != 2:
                    return
                pkg_name = arr[0]
                self.tag_data[pkg_name] = []
                sp2 = arr[1].split(", ")
                for a in sp2:
                    self.tag_data[pkg_name].append(a)

            except Exception as e:
                logger.error("Failed to split data: %s", e)

    def get_tags(self, pkg_name):
        try:
            pkgdata = self.tag_data[pkg_name]
        except KeyError:
            return []

        return pkgdata
