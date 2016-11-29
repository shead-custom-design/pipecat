"""Data logging library."""

from __future__ import absolute_import, division, print_function

import collections
import logging
import sys

import numpy
import pint

__version__ = "0.1.0-dev"

log = logging.getLogger(__name__)

units = pint.UnitRegistry()
quantity = units.Quantity

def dump(record, fobj=sys.stdout):
    """Dump a human-readable text representation of a record to a file-like object.

    Parameters
    ----------
    record: dict, required
        Dictionary of key-value pairs to be written-out.
    fobj: file-like object, optional
    """

    for key, value in sorted(record.items()):
        if isinstance(key, tuple):
            key = "/".join(key)
        fobj.write("%s: %s\n" % (key, value))
    fobj.write("\n")

def store(record, key, value):
    """Add a key-value pair to a record.

    Parameters
    ----------
    record: dict, required
        Dictionary of key-value pairs that constitute a record.
    key: string or tuple of strings, required
        Record key to be overwritten.
    value: object
        New record value.
    """

    if key in record:
        log.warning("Overwriting %s=%s with %s=%s", key, record[key], key, value)
    record[key] = value

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

