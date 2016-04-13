# MusicLibraryPy - Tools to analyse and repair/update music libraries
# Copyright (C) 2016 MusicLibraryPy
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
from .base import MusicLibraryBase
from ..album import Album


class MusicLibraryReport(MusicLibraryBase):
    """ Generate music library report """

    def run(self):
        """ Run """
        self.log.info('Iterating music library in "{path}"...'.format(
            path=self.args.path))

        for path, dirs, files in os.walk(self.args.path):
            # Only analyse leaf directories (those that only contain files)
            if len(dirs) < 1:

                # Read album
                album = Album(path, files)

                # Log album information
                self.log.info(album.info())

                # Log warnings
                for warning in album.warnings:
                    self.log.warning(warning)

                # Log errors
                for error in album.errors:
                    self.log.error(error)
