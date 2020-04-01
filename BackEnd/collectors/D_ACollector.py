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
import requests
import logging
import json
import time
from abc import ABC, abstractmethod


class D_ACollector(ABC):
    def __init__(self, d_a_root_src, d_a_root_raw,
                 repository_api_data_root_path, file_prefix):
        self.d_a_root_src = d_a_root_raw
        self.d_a_root_raw = d_a_root_src
        self.file_prefix = file_prefix
        self.conn = requests.Session()

        data_pattern = r"<define-tag (\S*?)>(.*?)<\/define-tag>"
        self.repository_api_data_root_path = repository_api_data_root_path

        self.data_pattern_matcher = re.compile(data_pattern, re.MULTILINE)
        date_pattern = r"[2-9][0-9]{3}"
        self.date_pattern_matcher = re.compile(date_pattern)

        # Setup logger
        logging.basicConfig(
            filename='./dvaf_backend.log',
            format='%(asctime)-15s -[%(module)s, %(funcName)s]:\t%(message)s')
        self.logger = logging.getLogger('d_aCollector')

    def get_d_as(self):
        return self.get_d_as_from_paths(
            self.get_d_a_repo_paths_from_remote_repo())

    def get_d_as_from_paths(self, paths):
        d_as_pool = {}

        for d_a_path in paths:
            d_a_data_file = self.get_data_from_url(
                self.d_a_root_src + d_a_path)
            d_a = self.get_d_a_from_data(d_a_data_file)

            if d_a is None:
                continue

            if d_a.db_d_a_id is None:
                file_name = \
                    self.get_d_a_name_from_url(d_a_path).split(".")[0]
                d_a_id = file_name[len(self.file_prefix):]
                # extract the id of the Dsa from the filename in case
                # it is not stated in the Data-File
                d_a.db_d_a_id = d_a_id

            if d_a.db_d_a_id in d_as_pool:
                d_a_attribute_names = [a for a in dir(d_a) if not a.startswith('__') and not callable(getattr(d_a, a))]

                for d_a_attribute_name in d_a_attribute_names:
                    d_a_attribute_value = getattr(d_a, d_a_attribute_name)

                    if d_a_attribute_value is not None:
                        setattr(d_as_pool[d_a_id], d_a_attribute_name,
                                d_a_attribute_value)
                # when d_a is already known, the the d_as have to be merged
                # in this implementation when a value of the d_a is not None
                # the Value in the "alternative d_a" is just overridden with
                # the value from the "d_a to be progressed"
            else:
                d_as_pool[d_a.db_d_a_id] = d_a

        return list(d_as_pool.values())

    def get_d_a_name_from_url(self, d_a_repo_path):
        return d_a_repo_path.split("/")[-1]

    def get_d_a_repo_paths_from_remote_repo(self):
        d_a_repo_dirs = self.get_gitlab_path_tree_from_remote_repo(
            self.d_a_root_raw,
            self.repository_api_data_root_path)
        d_a_year_paths = list(
            filter(lambda d_a_year_path: self.date_pattern_matcher.match(d_a_year_path.split("/")[-1]), d_a_repo_dirs))
        d_a_paths = []

        for d_a_year_path in d_a_year_paths:
            for d_a_repo_file_path in \
                    self.get_gitlab_path_tree_from_remote_repo(
                        self.d_a_root_raw, d_a_year_path):
                if d_a_repo_file_path is None or not self.get_d_a_name_from_url(d_a_repo_file_path).startswith(self.file_prefix):
                    continue  # not a subfolder or not data file
                d_a_paths += [d_a_repo_file_path]
        return d_a_paths

    @abstractmethod
    def get_d_a_from_data(self, d_a_data_file):
        pass

    def get_gitlab_path_tree_from_remote_repo(self, root_url, path):
        d_a_repo_dirs = []
        for page in range(1, 100):
            # needs to be split in pages,
            # because limit is 100 entrys per request
            page_data = self.get_data_from_url(root_url + "?path=" + path + "&page={0}&per_page=100".format(page))
            new_d_a_repo_dirs = json.loads(page_data)
            if len(new_d_a_repo_dirs) == 0:
                # reached end of files in directory
                break
            d_a_repo_dirs += new_d_a_repo_dirs

        return [d_a_repo_dir["path"]
                for d_a_repo_dir in d_a_repo_dirs if "path" in d_a_repo_dir]

    def get_data_from_url(self, url):
        download_failure_retrys = 0
        result = None
        if self.conn is None:
            self.conn = requests.Session()

        while download_failure_retrys < 30:
            # For stability, when an error occurs it is retried
            # to download and logged when the error persists
            try:
                result = self.conn.get(url).text
                return result
            except requests.Timeout:
                download_failure_retrys += 1
                time.sleep(2)
            except requests.TooManyRedirects:
                self.logger.log(logging.FATAL,
                                "BAD d_a ROOT URL: '{}' could not get any Data"
                                .format(url))
                break
            except requests.RequestException as e:
                self.logger.log(
                    logging.CRITICAL,
                    "URL '{}' Request could not"
                    " been completed due to: {}".format(url, e))
                download_failure_retrys += 1
                time.sleep(2)

        if download_failure_retrys >= 30:
            self.logger.fatal(
                "ROOT URL Request could not been completed due to many retrys")

        return result
