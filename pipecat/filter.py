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

"""Functions to filter records as they pass through a Pipecat pipe."""

from __future__ import absolute_import, division, print_function


def keep(source, key=None, value=None):
    """Discard all records that don't match the given criteria

    Examples
    --------

    Discard any record that doesn't have an 'id' key with value "GPGGA":

    >>> pipe = # Defined elsewhere
    >>> pipe = pipecat.filter.keep(pipe, key="id", value="GPGGA")
    >>> for record in pipe:
    ...     print record

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: string or tuple-of-strings, optional
        Records must contain this key or they will be discarded.
    value: optional.
        Records with field 'key' must match this value or they will be discarded.
    """
    for record in source:
        if key is not None and key not in record:
            continue
        if key is not None and value is not None and record[key] != value:
            continue
        yield record


def duplicates(source, key):
    """Discard records unless the given key value changes.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: string or tuple-of-strings, required
        Records will be discarded unless this key value changes.
    """

    initialized = False
    value = None
    for record in source:
        if initialized and record[key] == value:
            continue
        initialized = True
        value = record[key]
        yield record
