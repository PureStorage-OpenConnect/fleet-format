# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

import numpy as np
import os
from time import time
from fleetfmt import FileReader 
from pathlib import Path
from statistics import mean


def load_fleet_data(fleetfile, batch_keys):
    databuffer = reader.read(batch_keys)
    
    databuffer = reshape_batch(databuffer)


def reshape_batch(batch):
    """ Utility to reshape the batch in prep for Keras input """
    # The batch arrives as a list with batch_size lists of 15 np arrays.
    # We need a list of 5 np arrays, each of size (batch_size, X, 3),
    # where X is either 1248 for the first 4 elements and 5040 for the last.
    res = []
    for idx in range(0, 15, 3):
        tmp = [field[idx:idx+3] for field in batch]
        tmp = np.stack(tmp, axis=0)
        tmp = np.transpose(tmp, (0, 2, 1))
        res.append(tmp)

    return res


if __name__ == '__main__':

    durations = []
    batch_size = 512
    fleetfile = Path("./random_example.flt")
    
    ### Drop caches between test runs to ensure clean data load for performance timing
    print("Dropping caches") ### EMW
    os.system("bash -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")

    print("Starting key load")
    with fleetfile.open('rb') as fhandle, FileReader(fhandle) as reader:
        dkeys = reader.keys()
        dkeys = list(dkeys)

        print("Starting data load")
        for epochs in range(1):
            batch_id = 0
            for i in range(0, 10000, batch_size): ### EMW change from range(0, len(dkeys), batch_sz)
                batchstart = time()
                batch_keys = dkeys[i:i+batch_size]
                data_batch = load_fleet_data(fleetfile, batch_keys)
                durations.append(time()-batchstart)
                batch_id += 1
    print("\nbatch load durations:", durations)
    
    avgduration = round(mean(durations),3)
    print("\naverage read duration:", avgduration)

