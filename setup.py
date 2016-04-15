#!/usr/bin/env python

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

from distutils.core import setup


setup(
    name='MusicLibraryPy',
    version='0.1',
    description='Tools to analyse and repair/update music libraries',
    author='Rob Hardwick',
    author_email='robhardwick@gmail.com',
    url='https://github.com/robhardwick/music-library-py',
    scripts=[
        'tools/music-library-report',
        'tools/music-library-update',
    ],
    install_requires=[
        'mutagen>=1.31',
        'python-magic>=0.4.11',
    ],
    packages=['musiclibrary'])
