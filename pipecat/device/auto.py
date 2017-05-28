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

"""Data sources that retrieve on-board diagnostics from an automobile using OBD-II."""

from __future__ import absolute_import, division, print_function

import sys
import time

import obd as obdii

from pipecat import quantity, units
from pipecat.record import add_field


def obd(connection, commands=None, rate=quantity(5, units.second)):
    """Retrieve OBD-II data from an automobile.

    This component requires the `Python-OBD` module (http://python-obd.readthedocs.io).

    Parameters
    ----------
    connection: :class:`obd.OBD` instance, required.
    rate: time quantity, required
        Rate at which data will be retrieved.

    Yields
    ------
    records: dict
        Records will contain OBD-II data retrieved from an automobile computer.
    """

    # Caller must supply an obd.OBD instance that's already connected.
    if not (isinstance(connection, obdii.OBD) and connection.is_connected()):
        raise ValueError("A valid obd.OBD connection is required.")

    # Get the set of available commands.
    if commands is None:
        commands = []
        for command in connection.supported_commands:
            try:
                if command.mode not in [1]:
                    continue
                if command.pid in [0x00, 0x01, 0x02, 0x20, 0x40, 0x41]:
                    continue
                commands.append(command)
            except: # pylint: disable=bare-except
                pass

    rate = rate.to(units.seconds).magnitude

    while True:
        record = dict()
        for command in commands:
            sys.stdout.flush()
            try:
                response = connection.query(command)
                name = command.name.lower().replace("_", "-")
                add_field(record, name, response.value)
            except: # pylint: disable=bare-except
                pass

        yield record

        time.sleep(rate)
