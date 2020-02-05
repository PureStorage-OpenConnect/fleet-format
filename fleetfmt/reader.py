# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

""" Fleet Format File Reader """

from fleetfmt.base import _FileAccessorBase

import io

import pyarrow as pa

from .format import FILE_HEAD_SERDES, KEYENTRY_HEAD_SERDES, \
                    RECORD_HEAD_SERDES, SCHEMA_HEAD_SERDES
from .format import MAGIC

class FileReader(_FileAccessorBase):
    """Use this class with a file open in read mode to read either 
       keys or records from the file.

    Methods:
        keys(): Returns all keys stored in the file.
        read(keys): Returns the record value(s) for a key or list of keys.
    

    """
    def __init__(self, fh):
        super().__init__(fh)
        self._keymap = None
        
        self._read_header()
        self._read_schema()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return False

    def keys(self):
        """Returns all keys stored in the Fleet file.
        
        Returns:
            (set): A set of keys for all records in the file. 
            
        """
        # lazily read keytable on first call
        if self._keymap is None:
            self._read_keytable()

        return self._keymap.keys()

    def read(self, keys):
        """Returns the record value(s) for a key or list of keys.
        
        Args:
            keys : A single key or a list of keys wholse values should be 
                   read from file.

        Returns: 
            The record value(s) associated with the key(s).  
        
        """
        if isinstance(keys, list):
            return [self._read_record(key) for key in keys]
        else:
            return self._read_record(keys) 

    def _read_record(self, key):
        # lazily read keytable on first call
        if self._keymap is None:
            self._read_keytable()

        # get record offset and seek there
        roff = self._keymap[key]
        self._fh.seek(roff)

        # read record size (bytes)
        (rsize,) = RECORD_HEAD_SERDES.from_file(self._fh)
        buf = self._fh.read(rsize)

        # deserialize using pyarrow
        rec = pa.deserialize(buf)

        # return the non-key components of record
        return rec

    def _read_schema(self):
        # read schema bytes
        (hsize,) = SCHEMA_HEAD_SERDES.from_file(self._fh)
        buf = self._fh.read(hsize)

        # Odd -- pyarrow.read_schema wants a readable buffer, and a bytes
        # object is insufficient. So we wrap it back up to pull out the schema
        wrap = io.BufferedReader(io.BytesIO(buf))
        self._schema = pa.read_schema(wrap)
