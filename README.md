# Fleet File Format and Utilities

The *Fleet format* is a file format for structured data that's designed for 
high-performance data loading in machine learning workflows. Saving 
structured datasets as a Fleet file can improve input pipeline performance 
by improving data and key load efficiency. 

A Fleet file contains the data records from a single logical
schema (aka table), and each record can be identified by a unique, primary
_key_.

## User Guide

### Pre-requisites

- Python 3.6+
- (Recommended) A virtualenv setup for your project

### Installing

Until a PyPI package is uploaded, follow the developer process to build the
package.

    make init   # install pre-requisites (one-time only)
    make test
    make dist   # only if building a .whl is desired

### Examples

Create a new fleet file by appending (key, record) to the file

    with open(filename, 'wb') as fhandle, FileWriter(fhandle) as writer:
        writer.append('key1', [0, 1, 2, 4])
        writer.append('key2', [5, 6, 7, 8, 9, 10])

Read records from a fleet file

    with open(filename, 'rb') as fhandle, FileReader(fhandle) as reader:
        for key in reader.keys():
            rec = reader.read(key)
            # do something useful with rec

Append a new record to an existing fleet file
     
	 with open(filename, 'rb+') as fhandle, FileWriter(fhandle) as writer:
	     writer.append('key3', [11, 12])

Further examples can be found in the [examples](examples) folder.

<!--
### Data model
-->

### Reporting issues

Issue tracker: https://github.com/purestorage/fleetfmt/issues


## Why Another File Format?

### Requirements:

- Structured records (tables) accessed "row-at-a-time"
- Records have a data model with a primary key
- Datasets in the TB+ scale, key-space in the few GB scale
- Read-mostly workflows with infrequent updates
- Accessible from Python, with minimal dependencies (e.g., NumPy ok)
- Read access via sequential or random access (by key)

### Alternatives considered:

- HDF5
- NumPy arrays
- TFRecords
- Parquet/Orca
- Avro

<!--
### Performance benchmarks

## Developer Guide

## Format Internals
-->


