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

.. warning::
   Pickle files written using Python 2 cannot be read using Python 3, and vice-versa.

"""

from __future__ import absolute_import, division, print_function

import pickle

import pint

import pipecat.store


def write(source, fobj):
    """Append records to a pickle file."""
    with pipecat.store._FileHelper(fobj, "a+b") as fobj: # pylint: disable=redefined-argument-from-local
        for record in source:
            pickle.dump(record, fobj)
            fobj.flush()
            yield record


def read(fobj):
    """Read records from a pickle file."""
    with pipecat.store._FileHelper(fobj, "rb") as fobj: # pylint: disable=redefined-argument-from-local
        pint.set_application_registry(pipecat.units)
        try:
            while True:
                yield pickle.load(fobj)
        except EOFError:
            pass
