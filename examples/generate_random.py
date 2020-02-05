# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

# The mock dataset created for this example Fleet file mimics a ECG dataset. 
# In this example, each patient record includes results from 15 ECG leads. 
# Leads #1-12 each contain 1248 values, and leads #13-15 each contain 5040 values. 
#
# Rather than save these 15 results sets separately, we save each patient record 
# as a single list of 15 arrays, which simplifies data management and improves data
# load times during training.


from fleetfmt import FileWriter, FileReader
import numpy as np
from pathlib import Path

fleetfile = Path("./random_example.flt")

# Number of patient records 
numkeys = 10000

# Utility to create a test numpy array
def make_dataset():
    def _rand_vec(size):
        data = np.array(1000*np.random.random(size), dtype=np.float32)
        return data

    return [_rand_vec(1248) for _ in range(12)] + \
           [_rand_vec(5040) for _ in range(3)]

with fleetfile.open('wb') as fhandle, FileWriter(fhandle) as writer:
    for key in range(0, numkeys):
        writer.append(key, [*make_dataset()])



