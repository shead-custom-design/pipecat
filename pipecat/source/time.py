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

"""Data sources that provide information related to time."""

from __future__ import absolute_import, division, print_function

import time

import arrow

import pipecat.record

def timestamp(source, key="timestamp"):
    """Add a timestamp to every record returned from another source."""
    for record in source:
        pipecat.record.add_field(record, key, arrow.utcnow())
        yield record


def metronome(rate=pipecat.quantity(1.0, pipecat.units.seconds)):
    """Generate an empty record at fixed time intervals."""
    while True:
        yield dict()
        time.sleep(rate.to(pipecat.units.seconds).magnitude)


