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

"""Elegant, flexible data logging in Python for connected sensors and
instruments."""

from __future__ import absolute_import, division, print_function

import logging

import pint

__version__ = "0.2.0"

log = logging.getLogger(__name__)
""":class:`logging.Logger`: All pipecat logging output uses this logger.
"""

units = pint.UnitRegistry()
"""Provides units for defining and converting physical quantities.

Examples
--------
>>> charge = 330 * pipecat.units.milliamps * pipecat.units.hours
>>> temperature = pipecat.quantity(23, pipecat.units.degC)
>>> temperature.to(pipecat.units.degF)
<Quantity(73.4000004, 'degF')>
"""

quantity = units.Quantity
"""Used to create and store physical quantities.

Examples
--------
>>> timeout = pipecat.quantity(5, pipecat.units.minutes)
>>> charge = pipecat.quantity(330, pipecat.units.milliamps * pipecat.units.hours)
>>> latitude = pipecat.quantity(35.1 pipecat.units.degrees)
"""


