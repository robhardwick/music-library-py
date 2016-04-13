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

from logging import (
    getLogger,
    Formatter,
    StreamHandler,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    NOTSET
)


def getLog():
    """ Get logging object for use in command line scripts """

    # Create formatter
    formatter = LogFormatter()

    # Create handler to output to stderr
    handler = StreamHandler()
    handler.setFormatter(formatter)

    # Create logger
    logger = getLogger('MusicLibrary')
    logger.addHandler(handler)

    # Log records with a priority of "debug" or higher (i.e. everything)
    logger.setLevel(DEBUG)

    return logger


class LogFormatter(Formatter):
    """ Custom log formatter to alter level names and apply colour """
    LEVEL_MAP = {
        CRITICAL:   'crit',
        ERROR:      'err',
        WARNING:    'warn',
        INFO:       'info',
        DEBUG:      'dbg',
        NOTSET:     '????',
    }
    COLOUR_MAP = {
        CRITICAL:   '\033[31m',
        ERROR:      '\033[31m',
        WARNING:    '\033[33m',
        INFO:       '\033[32m',
        DEBUG:      '\033[34m',
        NOTSET:     '',
    }
    COLOUR_END = '\033[0m'

    def __init__(self):
        Formatter.__init__(
            self,
            '%(colour)s[%(asctime)s][%(level)-4s] %(message)s%(end)s',
            '%Y-%m-%dT%H:%M:%S'
        )

    def format(self, record):
        """ Alter log message level name """
        record.level = self.LEVEL_MAP[record.levelno]
        record.colour = self.COLOUR_MAP[record.levelno]
        record.end = self.COLOUR_END
        return Formatter.format(self, record)
