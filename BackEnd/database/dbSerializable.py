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
import logging

# setup logger
logger = logging.getLogger(__name__)
logger.propagate = False


class DBPatchFile:
    """Creates a DBPatchFile object. If path is not specified, \
        an empty patch file will be created.

    Keyword arguments:
    path -- the relative or absolute path to the patch file
    """

    def __init__(self, path=""):
        # setup logger
        self.logger = logging.getLogger(__package__)

        # if no path is given, we create an empty patch file
        if path == "":
            self.patches = json.loads("{}")
        else:
            try:
                file = open(path, "r")
                self.patches = json.loads(file.read())
                file.close()
            except Exception as e:
                self.logger.fatal("Could not open patch file: {}"
                                  .format(str(e)))
                return

        self.logger.info("Patch file <{}> loaded."
                         .format("EMPTY" if path == "" else path))

    def patch(self, serializable):
        """Checks if the patch file has an entry with the key of
        serializable.
        If it is found, the attributes in serializable will be
        replaced.

        Keyword arguments:
        serializable -- an instance of DBSerializable
        """
        # find the entry in the patch file
        pk = serializable.get_primary_key()

        if pk not in self.patches:
            return

        for k, v in self.patches[pk].items():
            serializable.patch_attribute(k, v)


class DBSerializable:
    """This is the super class for all objects that can be queried from
    and written to the database. All attributes which shall be written
    to the database must start "db_".

    Keyword arguments:
    primary_key_name -- the name of the primary key with which this
    object
    can be identiefied in the database.
    """
    patch_file = DBPatchFile()

    def __init__(self, primary_key_name):
        self.primary_key_name = primary_key_name

    """Returns the primary key name. The primary key name can be set
    in __init__()."""
    def get_primary_key_name(self):
        return self.primary_key_name

    """Returns the primary key value."""
    def get_primary_key(self):
        return self.__dict__["db_" + self.get_primary_key_name()]

    def to_dict(self):
        """Returns the dictionary representation of this object."""
        dic = dict()

        for k, v in self.__dict__.items():
            # only attributes starting with db_ will be serialized
            if not k.startswith("db_"):
                continue

            val = v

            if isinstance(v, DBSerializable):
                val = v.to_dict()

            # val must support a decent representation
            dic[k[3:]] = val

        return dic

    @classmethod
    def from_dict(cls, dic):
        """Creates the object from the dictionary representation.
        As this can vary whith different objects, this method should
        be overriden in subclasses as needed.

        Keyword arguments:
        dic -- the dictionary representation of the object
        """
        # If the default implementation is used then the names
        # of parameters are important!
        return cls(**dic)

    @classmethod
    def from_list(cls, ls):
        """A short way of converting a list of dictionary
        representations (as usually
        returned by the database) to the corresponding objects.
        The list must only contain dictionary representations of
        one type.

        Keyword arguments:
        ls -- the list of dictionary representations
        """
        return map(lambda e: cls(**e), ls)

    @classmethod
    def set_patch_file(cls, path):
        """Sets the patch file to be used.

        Keyword arguments:
        path -- the file path to the patch file
        """
        cls.patch_file = DBPatchFile(path)

    def patch(self):
        """Reads the patch information from the patch file and
        inserts it, i.e. replaces all of it's attributes with values
        found in the patch file.
        """
        self.patch_file.patch(self)

    def patch_attribute(self, name, value):
        """Replace a single attribute called name with value.

        Keyword arguments:
        name -- name of the attribute
        value -- value of the attribute
        """
        self.__dict__["db_" + name] = value
