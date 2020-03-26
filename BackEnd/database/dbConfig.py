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
import json
import os
import logging

DB_DEFAULT_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "/dbconfig.json"


class DBConfigProps:
    """Represents the properties read from a config file.
    A property can be simply accessed with DBConfigProps().prop_name."""
    DEFAULT_PROPS = {
        "port": 27017,
        "placeholder_1": "MyString",
        "placeholder_2": 123456,
        "placeholder_3": 3.14
    }

    def set_default_config(self):
        """Initializes the attributes with DEFAULT_PROPS."""
        for key, val in self.DEFAULT_PROPS.items():
            self.__setattr__(key, val)

    def read_json_dict(self, json_dict):
        """Reads the properties from a json dict and replaces its own attribute
        values with the ones from the dict. Type checking is done as well."""

        for k in set(self.DEFAULT_PROPS.keys()) \
                .intersection(set(json_dict.keys())):
            if isinstance(self.__getattribute__(k), type(json_dict[k])):
                self.__setattr__(k, json_dict[k])

    def as_dict(self):
        """Returns a dictionary representation of the properties."""
        return dict(zip(self.DEFAULT_PROPS.keys(),
                        map(self.__getattribute__,
                            self.DEFAULT_PROPS.keys())))

    def __init__(self):
        self.set_default_config()


class DBConfig:
    """The corresponding object to a config file. The config file must be
    in a simple json format: { ... \"key\": value, ... }.
    Properties can be set and queried with DBConfig().props.prop_name."""

    def __init__(self, path=DB_DEFAULT_CONFIG_PATH):
        # config file for now is in the same folder as this file
        self.path = path

        # setup logger
        self.logger = logging.getLogger(__package__)

        # default properties
        self.props = DBConfigProps()
        self.config_file = None

        # try to find config file and read it
        try:
            # does it exist?
            self.config_file = open(self.path, "r")

            # read config file
            json_obj = json.loads(self.config_file.read())
            self.props.read_json_dict(json_obj)

            self.config_file.close()
        except FileNotFoundError:
            try:

                self.save_config()
            except Exception as e:
                # couldn't do anything
                self.logger.fatal("could not find or create database config file: {}".format(e))
                return
        except Exception as e:
            self.logger.fatal("could not read config file: {}".format(e))

        self.logger.debug("current database configuration: {}".format(
            self.props.as_dict()))

    def save_config(self):
        """Saves the changed properties to the config file."""
        try:
            self.config_file = open(self.path, "w")
            self.config_file.write(json.dumps(self.props.as_dict()))
            self.config_file.close()
        except Exception as e:
            self.logger.fatal("could not save database config")
