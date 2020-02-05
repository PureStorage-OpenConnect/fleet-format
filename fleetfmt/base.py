# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

""" Fleet Format _FileAccessorBase (parent class) """

import io

import pyarrow as pa

from .format import FILE_HEAD_SERDES, KEYENTRY_HEAD_SERDES, \
                    RECORD_HEAD_SERDES, SCHEMA_HEAD_SERDES
from .format import MAGIC, VERSION


class Error(Exception):
    """Base class for custom exceptions"""
    pass

class VersionUnsupportedError(Error):
    """Raised when Fleet version in header doesn't match a supported version"""
    pass

class MagicUnsupportedError(Error):
    """Raised when MAGIC value in header doesn't return a supported value"""
    pass

class _FileAccessorBase:
    def __init__(self, fh):
        self._fh = fh
        self._magic = ''
        self._key_count = 0
        self._key_start = 0
        self._version = 0
        self._schema = None # infer from first record
        # Note: self._keymap is set during initialization of child classes 

    def _read_header(self):
        # rewind file to beginning
        self._fh.seek(0)

        (magic, version, key_count, key_start) = \
            FILE_HEAD_SERDES.from_file(self._fh)

        # validate file format
        self._magic = magic.decode('ascii')
        if self._magic != MAGIC:
            raise MagicUnsupportedError
        self._version = version
        if self._version != VERSION:
            raise VersionUnsupportedError
        self._key_count = key_count
        self._keytable_offset = key_start

    def _read_keytable(self):
        self._keymap = {}

        # jump to the start of the keytable
        self._fh.seek(self._keytable_offset)

        keymapser = self._fh.read()
        
        keymapdes = pa.deserialize(keymapser)

        self._keymap = dict(keymapdes)
