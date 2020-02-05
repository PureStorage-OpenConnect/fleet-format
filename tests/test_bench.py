# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

"""
Benchmark Fleet format APIs
"""

from fleetfmt import FileWriter, FileReader

import io
import pytest

def read_in_order(fhandle):
    with FileReader(fhandle) as reader:
        for key in reader.keys():
            reader.read(key)
        count = len(reader.keys())
    return count

@pytest.mark.parametrize("key_count", [1000])
def test_bench_simple(key_count, benchmark):
    memfile = io.BytesIO()

    with FileWriter(memfile) as writer:
        for key in range(key_count):
            writer.append(str(key), [int(key)])

    res = benchmark(read_in_order, memfile)
    assert res == key_count
