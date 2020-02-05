# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

""" Fleet Format File Writer """

from fleetfmt.base import _FileAccessorBase

import numpy as np
import pyarrow as pa

from .format import FILE_HEAD_SERDES, KEYENTRY_HEAD_SERDES, \
                    RECORD_HEAD_SERDES, SCHEMA_HEAD_SERDES
from .format import MAGIC, VERSION

def _arrow_type_from_numpy(val):
    if np.ndim(val) == 0:
        arrv = pa.array([val])
        return arrv.type
    else:
        arrv = pa.array(val)
        return pa.list_(arrv.type)

def _infer_schema(record):
    fields = []
    for idx, val in enumerate(record):
        name = "_{}".format(idx)
        typ = _arrow_type_from_numpy(val)
        fields.append(pa.field(name, typ))
    return pa.schema(fields)

class FileWriter(_FileAccessorBase):
    """Use this class with a file open in write mode to write 
       (key, record) pairs to the file.

    Methods:
         append(key, record): Appends a (key, record) pair to the file. 

    """
    def __init__(self, fh):
        super().__init__(fh)
        self._keymap = {}

        # if header exists, read it and write a temp editing header, 
        # to be revised on close 
        try:
            self._read_header()
            self._read_keytable()
            self._write_header(-1)
            self._fh.seek(self._key_start)
        # if no header exists yet, write an temp initial header, 
        # to be revised on close
        except:
            self._write_header(0)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self._finish()
        return False

    def append(self, key, record):
        """Appends a (key, record) pair to the file. 


        """
        if not self._schema:
            self._schema = _infer_schema(record)
            self._write_schema()

        # append record to datatmp
        offset = self._write_record(record)

        # add key and offset ptr to in-memory keymap dictionary
        self._keymap[key] = offset

    def _finish(self):
        # append key list
        key_start = self._write_key_table()

        # re-write header with key metadata
        self._write_header(key_start)

        # outer context that provided self._fh must close it

    def _write_header(self, key_start):
        header = FILE_HEAD_SERDES.to_bytes(MAGIC.encode('ascii'),
                                           VERSION,
                                           len(self._keymap),
                                           key_start)
        self._fh.seek(0)
        self._fh.write(header)

    def _write_schema(self):
        sbuf = self._schema.serialize()
        hbuf = SCHEMA_HEAD_SERDES.to_bytes(sbuf.size)
        self._fh.write(hbuf)
        self._fh.write(sbuf)

    def _write_record(self, record):
        # capture location of start of record
        loc = self._fh.tell()

        # serialize record and write to file
        buf = pa.serialize(record).to_buffer()
        head = RECORD_HEAD_SERDES.to_bytes(buf.size)
        self._fh.write(head)
        self._fh.write(buf)

        # return starting location
        return loc

    def _write_key_table(self):
        # note the end of the record stream as the start of the
        # key table, to be written into the file header
        start_off = self._fh.tell()

        kbuf = pa.serialize(self._keymap).to_buffer()

        self._fh.write(kbuf)

        return start_off
