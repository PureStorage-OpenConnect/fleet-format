# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

"""
Test Fleet format reader/writer interface
"""

from fleetfmt import FileWriter, FileReader

import numpy as np
import pytest

def test_basic(tmp_path):
    """ Test that we can read the entirety of a simple file"""
    # Write file
    pfile = tmp_path / "test.flt"
    with pfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
        writer.append(100, [1, 2, 3])

    # Read and validate
    with pfile.open('rb') as fhandle, FileReader(fhandle) as reader:
        assert set(reader.keys()) == {100}
        rec = reader.read(100)
        assert len(rec) == 3
        assert rec == [1, 2, 3]

def test_read_twice(tmp_path):
    # Write file
    pfile = tmp_path / "test.flt"
    with pfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
        writer.append(100, [1, 2, 3])

    with pfile.open('rb') as fhandle:
        with FileReader(fhandle) as reader:
            assert reader.keys() == {100}

        with FileReader(fhandle) as reader:
            assert reader.keys() == {100}

def test_read_complex(tmp_path):
    """ Test that we can read a set of keys """
    # Write file
    pfile = tmp_path / "test.flt"
    with pfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
        writer.append(100, [1, 2, 3])
        writer.append(101, [4, 5, 6])
        writer.append("alpha", ["7", "8", "9"])

    # Read and validate
    with pfile.open('rb') as fhandle, FileReader(fhandle) as reader:
        assert set(reader.keys()) == {100, 101, "alpha"}
        rec = reader.read([100, 101, "alpha"])
        assert np.array(rec).shape == (3,3)
        assert rec[0] == [1, 2, 3]
        assert rec[1] == [4, 5, 6]
        assert rec[2] == ["7", "8", "9"]

def test_append_to_new(tmp_path):
    """Test that we can append to an empty file"""
    # Use append to write initial records into a new file (opened in 'wb' mode)
    pfile = tmp_path / "test.flt"
    with pfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
        a = writer.append(100, [0])
        b = writer.append(101, [1])
    # Read and validate
    with pfile.open('rb') as fhandle, FileReader(fhandle) as reader:
        assert set(reader.keys()) == {100, 101}
        assert reader.read(101) == [1]

def test_append_to_existing(tmp_path):
    """ Test that we can add new records to existing file """
    # Write file
    pfile = tmp_path / "test.flt"
    with pfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
        a = writer.append(100, [0])
        b = writer.append(101, [1])
        c = writer.append(102, [2])
    # Insert new record to existing file 
    with pfile.open('rb+') as fhandle, FileWriter(fhandle) as writer:
        d = writer.append(103, [3])
    # Read and validate
    with pfile.open('rb') as fhandle, FileReader(fhandle) as reader:
        assert set(reader.keys()) == {100, 101, 102, 103}
        assert reader.read(103) == [3]

def test_invalid_read_inputs(tmp_path):
    """ Test that exception is raised for invalid reader.read() inputs """
    # Raise exception for malformed read requests
    with pytest.raises(Exception):
        assert reader.read(1.234)
