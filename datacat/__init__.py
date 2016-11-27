"""Data logging library."""

from __future__ import absolute_import, division, print_function

import collections
import logging
import sys

import numpy
import pint

__version__ = "0.1.0-dev"

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

units = pint.UnitRegistry()
quantity = units.Quantity

def dump(observation, stream=sys.stdout):
    """Dump a human-readable text representation of an observation to a stream.

    Parameters
    ----------
    observation: dict, required
        Dictionary of key-value pairs to be written-out.
    stream: file-like object, optional
    """

    for key, value in sorted(observation.items()):
        if isinstance(key, tuple):
            key = "/".join(key)
        stream.write("%s: %s\n" % (key, value))
    stream.write("\n")

def store(observation, key, value):
    """Add a key-value pair to an observation.

    Parameters
    ----------
    observation: dict, required
        Dictionary of key-value pairs that constitute an observation.
    key: string or tuple of strings, required
        Observation key to be overwritten.
    value: object
        New observation value.
    """

    if key in observation:
        log.warning("Overwriting %s=%s with %s=%s", key, observation[key], key, value)
    observation[key] = value

class Table(object):
    def __init__(self):
        self._columns = collections.OrderedDict()

    def __len__(self):
        for column in self._columns.values():
            return len(column)
        return 0

    def __getitem__(self, key):
        values = self._columns[key]
        if isinstance(values[0], quantity):
            values = quantity(numpy.array([value.magnitude for value in values]), values[0].units)
        else:
            values = numpy.array(values)
        return values

    def append(self, record):
        for key, value in record.items():
            if key not in self._columns:
                self._columns[key] = []
            self._columns[key].append(value)

    def keys(self):
        return self._columns.keys()

    def items(self):
        return self._columns.items()

    def values(self):
        return self._columns.values()

