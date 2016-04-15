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

from .base import MusicLibraryBase


class MusicLibraryUpdate(MusicLibraryBase):
    """ Fix/repair contents of music library """

    def run(self):
        """ Run """
        self.log.error('The "update" action has not been implemented')
