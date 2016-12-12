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

"""Data sources that retrieve information from clocks."""

from __future__ import absolute_import, division, print_function

import time

import pipecat

def metronome(rate=pipecat.quantity(1.0, pipecat.units.seconds)):
    """Generate an empty record at fixed time intervals using the host clock.

    Typically, you would use functions such as
    :func:`pipecat.utility.add_field` or :func:`pipecat.utility.add_timestamp`
    to populate the (otherwise empty) records.

    Examples
    --------

    If you want to know what time it is, at 5-minute intervals:

    >>> pipe = pipecat.device.clock.metronome(pipecat.quantity(5, pipecat.units.minutes))
    >>> pipe = pipecat.utility.add_timestamp(pipe)
    >>> for record in pipe:
    ...   print record

    Parameters
    ----------
    rate: time quantity, required
        The amount of time to wait between records.

    Yields
    ------
    records: dict
        Yields an empty record at fixed time intervals.
    """
    delay = rate.to(pipecat.units.seconds).magnitude
    last_time = time.time()
    while True:
        yield dict()
        next_time = last_time + delay
        time.sleep(next_time - time.time())
        last_time = next_time


