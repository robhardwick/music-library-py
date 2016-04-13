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
import magic
import mutagen


class AudioFile(object):
    """ Analyse audio file """
    METADATA = {
        'artist': (
            'TPE1',
            'ARTIST',
            'Artist',
            '\xa9ART',
            'Author',
            'TSOP',
            'ARTISTSORT',
            'soar',
        ),
        'album_artist': (
            'TPE2',
            'ALBUMARTIST',
            'Album Artist',
            'aART',
            'TSO2',
            'TXXX:ALBUMARTISTSORT',
            'ALBUMARTISTSORT',
            'soaa',
        ),
        'album': (
            'TALB',
            'ALBUM',
            'Album',
            'album',
            '\xa9alb',
            'TSOA',
            'ALBUMSORT',
            'soal',
        ),
        'title': (
            'TIT2',
            'TITLE',
            'Title',
            '\xa9nam',
            'TSOT',
            'TITLESORT',
            'sonm',
        ),
    }
    REQUIRED_PROPERTIES = ('artist', 'album',)

    def __init__(self, path, filename):
        """ Read audio file information """

        # Get full path to file
        filepath = os.path.join(path, filename)

        # Open file with mutagen
        mfile = mutagen.File(filepath)
        if mfile is None:
            # Raise exception if not a valid audio file
            mime_type = magic.from_file(filepath, mime=True)
            raise NotAudioException(filename, mime_type)

        # Get audio file MIME type
        self.mime_type = mfile.mime[0]

        # Set lossless flag
        self.lossless = self.is_lossless(mfile)

        # Set audio file metadata
        for key, value in self.get_metadata(mfile).iteritems():
            setattr(self, key, value)

        # Check required metadata is set
        missing = []
        for key in self.REQUIRED_PROPERTIES:
            if getattr(self, key, None) is None:
                missing.append(key)

        # Raise exception if any required metadata is missing
        if len(missing) > 0:
            raise MissingMetadataException(filename, missing, keys)

    def is_lossless(self, mfile):
        """ Determine if the audio file is lossless or lossy """
        return (
            # FLAC, OggFLAC and AIFF are lossless
            isinstance(mfile, (
                mutagen.oggflac.OggFLAC,
                mutagen.flac.FLAC
            )) or \
            # MP4s using the ALAC codec are lossless too
            (
                isinstance(mfile, mutagen.mp4.MP4) and \
                getattr(mfile.info, 'codec', None) == 'alac'
            )
        )

    def get_metadata(self, mfile):
        """ Get audio file metadata """
        tags = {}

        # Iterate through metadata properties
        for key, tag_names in self.METADATA.items():
            tags[key] = None

            # Attempt to get value for this property using all known tag names
            for tag_name in tag_names:
                try:
                    tags[key] = unicode(mfile[tag_name][0])
                    break
                except KeyError:
                    pass

        return tags

    def __repr__(self):
        """ String representation of this audio file """
        return '{artist} / {album} / {title} ("{mime}", {compression})'.format(
            compression='lossless' if self.lossless else 'lossy',
            **self.__dict__)


#
# Exceptions
#

class NotAudioException(Exception):
    """ Non-audio file """

    def __init__(self, filename, mime_type):
        self.filename = filename
        self.mime_type = mime_type

    def __str__(self):
        return 'Non-audio file type "{mime_type}" for "{filename}"'.format(
            **self.__dict__)


class MissingMetadataException(Exception):
    """ Audio file with missing required metadata (e.g. artist or title) """

    def __init__(self, filename, missing, keys):
        self.filename = filename
        self.missing = missing
        self.keys = keys

    def __str__(self):
        return 'Missing {missing} for "{filename}" (available: {keys})'.format(
            missing=missing, filename=filename, keys=mfile.keys())
