# MusicLibraryPy - Tools to analyse and repair/update music libraries
# Copyright © 2016 Rob Hardwick
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os
from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser, ArgumentTypeError
from .log import getLog


class MusicLibraryBase(object):
    """ Parse command line arguments and run specified action """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Initialise script """

        # Get logger
        self.log = getLog()

        # Create argument parser
        self.parser = ArgumentParser()
        self.parser.add_argument(
            'path',
            type=self.valid_directory,
            metavar='PATH',
            help='Path to music library root directory')

        # Parse arguments
        self.args = self.parser.parse_args()

    def valid_directory(self, path):
        """ Ensure the given path is a valid and accessible directory """
        if not os.path.exists(path):
            error = 'Path does not exist'
        elif not os.path.isdir(path):
            error = 'Path is not a valid directory'
        elif not os.access(path, os.R_OK):
            error = 'Path is not accessible'
        else:
            return path
        raise ArgumentTypeError('{error}: {path}'.format(
            error=error, path=path))

    @abstractmethod
    def run(self):
        pass
