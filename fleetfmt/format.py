# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

""" File format utilities """

import struct

MAGIC = 'FLTF'
VERSION = 1

# Helper class that defines serialization and deserialization for various
# fields in the file format.
class _SerDes:
    def __init__(self, fmt):
        self._fmt = fmt
        self._size = struct.calcsize(fmt)

    def to_bytes(self, *args):
        """
        Converts `args` into bytes, according to defined format.
        """
        return struct.pack(self._fmt, *args)

    def from_file(self, fhandle):
        """
        Reads and returns a tuple of values from file handle `fhandle`,
        according to defined format.
        """
        buf = fhandle.read(self._size)
        return struct.unpack(self._fmt, buf)

# File header format
# <  = little endian
# 4s = 4-character string with MAGIC
# I  = 4-byte integer with VERSION
# Q  = 8-byte number of keys
# Q  = 8-byte offset to start of key table
FILE_HEAD_SERDES = _SerDes("<4sIQQ")

# Key table entry format
# <  = little endian
# I  = 4-byte integer with size of key buffer
# Q  = 8-byte offset to record data
#
# Each key-table entry has this metadata, followed by the
# pyarrow-serialized key itself
KEYENTRY_HEAD_SERDES = _SerDes("<IQ")

# Record entry format
# <  = little endian
# I  = 4-byte integer with size of record buffer
#
# Each record entry has this metadata, followed by the
# pyarrow-serialized record itself
RECORD_HEAD_SERDES = _SerDes("<I")

# Schema entry format
# <  = little endian
# I  = 4-byte integer with size of schema buffer
#
# The schema is serialized with this header followed by the
# pyarrow-serialized schema itself
SCHEMA_HEAD_SERDES = _SerDes("<I")
