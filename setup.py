# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fleetfmt",
    version="0.7.0",
    author="Pure Storage",
    description="Fleet format file library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purestorage/fleetfmt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyarrow>=0.15.0',
        'numpy>=1.17.3',
    ],
    extras_require={
        "dev": [
            'wheel>=0.33.0',
            'pytest>=3',
            'pytest-benchmark>=3.2.2',
        ],
    },
)
