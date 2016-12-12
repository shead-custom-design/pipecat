# Copyright 2016 Timothy M. Shead
#
# This file is part of Pipecat.
#
# Pipecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pipecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pipecat.  If not, see <http://www.gnu.org/licenses/>.

"""Functions for manipulating data records."""

from __future__ import absolute_import, division, print_function

import sys

import pipecat

def add_field(record, key, value):
    """Add a key-value pair to a record.

    Parameters
    ----------
    record: dict, required
        Dictionary of key-value pairs that constitute a record.
    key: :ref:`Record key <record-keys>`, required
        Record key to be overwritten.
    value: object
        New record value.
    """

    if key in record:
        pipecat.log.warning("Overwriting %s=%s with %s=%s", key, record[key], key, value)
    record[key] = value

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

