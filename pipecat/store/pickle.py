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

"""Functions for reading and writing data using Python pickle files.
"""

from __future__ import absolute_import, division, print_function

import pickle

import pipecat.compatibility

def write(source, fobj):
    """Append records to a pickle file."""
    def implementation(source, fobj): # pylint: disable=missing-docstring
        for record in source:
            pickle.dump(record, fobj)
            yield record

    if isinstance(fobj, pipecat.compatibility.string_type):
        with open(fobj, "a+b") as fobj:
            for record in implementation(source, fobj):
                yield record
    else:
        for record in implementation(source, fobj):
            yield record


def read(fobj):
    """Read records from a pickle file."""
    def implementation(fobj): # pylint: disable=missing-docstring
        try:
            while True:
                yield pickle.load(fobj)
        except EOFError:
            pass

    if isinstance(fobj, pipecat.compatibility.string_type):
        with open(fobj, "rb") as fobj:
            for record in implementation(fobj):
                yield record
    else:
        for record in implementation(fobj):
            yield record
