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

from .file import AudioFile, NotAudioException, MissingMetadataException


class Album(object):
    """ Validate a give list of files as a music album """
    REQUIRED_PROPERTIES = {
        'mime_type':    '{path}: Mixing different formats ({values})',
        'artist':       '{path}: Multiple artists ({values})',
        'album':        '{path}: Different album names ({values})',
    }

    def __init__(self, path, files):
        """ Set initial values and read album """
        self.path = path
        self.mime_type = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'
        self.files = []
        self.errors = []
        self.warnings = []

        # Read album
        for filename in files:
            try:
                audio_file = AudioFile(path, filename)

            # Ignore any non-audio files
            except NotAudioException as e:
                self.warnings.append(unicode(e))

            # Log errors for missing
            except MissingMetadataException as e:
                self.errors.append(unicode(e))

            else:
                # add to album's audio file list
                self.files.append(audio_file)

        # Set required properties or, if missing, add an error
        for key, error in self.REQUIRED_PROPERTIES.iteritems():
            self.set_property(key, error)

    def set_property(self, key, error):
        """ Set metadata property if consistent across a;; album's files """
        values = set((getattr(audio_file, key) for audio_file in self.files))
        if len(values) < 1:
            self.errors.append('{path}: No values for {key}'.format(
                path=self.path, key=key))
        elif len(values) > 1:
            self.errors.append(error.format(
                path=self.path, values=', '.join(values)))
        else:
            setattr(self, key, values.pop())

    def info(self):
        """ Return string of album information """
        return '{artist} - {album}'.format(**self.__dict__)
