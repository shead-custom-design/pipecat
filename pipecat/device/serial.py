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

"""Functions for working with serial ports.
"""

from __future__ import absolute_import, division, print_function

import time

import serial

import pipecat.utility


def readline(*args, **kwargs):
    """Reliably read lines from a serial port.

    Accepts the same parameters as :func:`serial.serial_for_url`, plus the following:

    Parameters
    ----------
    poll: time quantity, optional
        Time to wait between failures.

    Yields
    ------
    records: dict
        Records will contain each line of text read from the port.
    """
    poll = kwargs.pop("poll", pipecat.quantity(5, pipecat.units.seconds)).to(pipecat.units.seconds).magnitude

    while True:
        try:
            pipe = pipecat.utility.readline(serial.serial_for_url(*args, **kwargs))
            for record in pipe:
                yield record
        except Exception as e:
            pipecat.log.error(e)
            time.sleep(poll)
