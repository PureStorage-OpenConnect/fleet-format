# Copyright 2020 Pure Storage Inc. 
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================

.PHONY: dist test bench init clean

INTERMED := build .eggs fleetfmt.egg-info

dist:
	python setup.py sdist bdist_wheel
	rm -rf $(INTERMED)

test:
	python -m pytest --benchmark-skip tests 

bench:
	python -m pytest --benchmark-only tests

init:
	pip install -e ".[dev]"

clean:
	rm -rf dist $(INTERMED)
