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

"""Convenience functions for working with data sources."""

from __future__ import absolute_import, division, print_function

import arrow
import six

import pipecat.record


def add_field(source, key, value):
    """Adds a key-value pair to every record returned from a source.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, required
    value: any value.

    Yields
    ------
    record: dict
        Input records containing an additional field `key` with value `value`.
    """
    for record in source:
        pipecat.record.add_field(record, key, value)
        yield record


def add_timestamp(source, key="timestamp"):
    """Add a timestamp to every record returned from a source.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, optional

    Yields
    ------
    record: dict
        Input records containing an additional field `key` with a :class:`arrow.arrow.Arrow` UTC timestamp value.
    """
    for record in source:
        pipecat.record.add_field(record, key, arrow.utcnow())
        yield record


def extract_quantities(source, value="value", units="units"):
    """Convert values with separate magnitude / units data into :class:`pipecat.quantity` instances.

    If a field value is a dict containing `value` and `units` keys, it will be
    replaced with a matching :class:`pipecat.quantity`.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    value: :ref:`Record key <record-keys>`, optional
    units: :ref:`Record key <record-keys>`, optional

    Yields
    ------
    record: dict
        Input records with field values converted to :class:`pipecat.quantity`
        instances.
    """
    for record in source:
        for k, v in record.items():
            if isinstance(v, dict) and value in v and units in v:
                record[k] = pipecat.quantity(v["value"], v["units"])
        yield record


def promote_field(source, key):
    """Promote key-value pairs from one field into their own fields.

    The field `key` must exist and contain a dict or dict-like object.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, required

    Yields
    ------
    record: dict
        Input records containing additional fields promoted from the value stored in `key`.
    """
    for record in source:
        for k, v in record[key].items():
            pipecat.record.add_field(record, k, v)
        yield record


def readline(fobj, encoding="utf-8"):
    """Extract lines from a file or file-like object.

    Parameters
    ----------
    fobj: file-like object, required
        This could be an open file, instance of :class:`io.StringIO`, a serial
        connection, or any other object from which lines of text can be read.

    Yields
    ------
    record: dict
        Records containing a "string" field that stores one line of text.
    """
    def line_iterator(fobj):
        if hasattr(fobj, "readline"):
            while True:
                line = fobj.readline()
                if not line:
                    break
                yield line
        else:
            for line in fobj:
                yield line

    for line in line_iterator(fobj):
        if isinstance(line, six.binary_type):
            line = line.decode(encoding)

        record = {}
        pipecat.record.add_field(record, "string", line)
        yield record


def remove_field(source, key):
    """Removes a key-value pair from every record returned by a source.

    Records that don't contain `key` are returned unmodified (this is not
    an error condition).

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, required
        The field to be removed.

    Yields
    ------
    record: dict
        Input records with the `key` field removed.
    """
    for record in source:
        pipecat.record.remove_field(record, key)
        yield record


def split_keys(source, delimiter):
    """Convert flat keys into hierarchical keys using a delimiter.

    This is useful working with data such as JSON that can't represent
    hierarchical keys explicitly.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    delimiter: str, required

    Yields
    ------
    record: dict
        Input records with keys containing the delimiter converted into hierarchical keys.
    """
    for record in source:
        output = {}
        for key, value in record.items():
            key = key.split(delimiter)
            key = tuple(key) if len(key) > 1 else key[0]
            pipecat.record.add_field(output, key, value)
        yield output


def trace(source, name=None):
    """Log the behavior of a source for debugging.

    Use :func:`pipecat.utility.trace` to log the behavior of another record
    generator, including the records it generates, any exceptions thrown, and
    notifications when it starts and finishes.  Records are passed through
    this function unmodified, so it can be inserted into an existing pipe
    without altering its behavior.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required

    Yields
    ------
    record: dict
        Unmodified input records.
    """
    if name is None:
        name = source.__name__

    pipecat.log.debug("%s started", name)

    try:
        for record in source:
            pipecat.log.debug("%s record: %s", name, record)
            yield record
    except GeneratorExit:
        pass

    except Exception as e:
        pipecat.log.debug("%s exception: %s %s", name, type(e), e)

    pipecat.log.debug("%s finished", name)
