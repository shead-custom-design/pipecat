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

"""Data sources that retrieve motion information from portable devices such as smartphones."""

from __future__ import absolute_import, division, print_function

from pipecat import quantity, units
from pipecat.record import add_field


def ios(rate=quantity(1, units.second)):
    """Retrieve motion information from an iOS device.

    This component requires the `motion` module provided by Pythonista.

    Parameters
    ----------
    rate: time quantity, required
        Rate at which motion data will be retrieved.

    Yields
    ------
    records: dict
        Records will contain information including the current acceleration due to gravity and the user, along with device attitude.
    """

    import time
    import motion # pylint: disable=import-error

    rate = rate.to(units.seconds).magnitude

    motion.start_updates()

    try:
        while True:
            gravity = quantity(motion.get_gravity(), units.meters * units.seconds * units.seconds)
            acceleration = quantity(motion.get_user_acceleration(), units.meters * units.seconds * units.seconds)
            attitude = quantity(motion.get_attitude(), units.radians)

            record = dict()
            add_field(record, ("gravity", "x"), gravity[0])
            add_field(record, ("gravity", "y"), gravity[1])
            add_field(record, ("gravity", "z"), gravity[2])

            add_field(record, ("acceleration", "x"), acceleration[0])
            add_field(record, ("acceleration", "y"), acceleration[1])
            add_field(record, ("acceleration", "z"), acceleration[2])

            add_field(record, ("attitude", "roll"), attitude[0])
            add_field(record, ("attitude", "pitch"), attitude[1])
            add_field(record, ("attitude", "yaw"), attitude[2])

            yield record

            time.sleep(rate)

    except GeneratorExit:
        motion.stop_updates()
