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

"""Data sources that retrieve information from battery chargers."""

from __future__ import absolute_import, division, print_function

from pipecat import quantity, units
from pipecat.record import add_field

def icharger208b(source):
    """Read data from an iCharger 208B battery charger.

    Logs data events emitted by the charger during charge, discharge, etc.  Likely works with other
    models from iCharger, but this is untested.  Consider :ref:`submitting-feedback` to let us know.

    This model battery charger comes with USB cable that provides serial-over-USB communication with
    the host computer.  To connect with the charger, you'll need to open a handle to the appropriate
    serial port, which will vary between platforms and based on the number and configuration of devices
    currently connected.

    Examples
    --------

    Open a serial port on a Mac OSX computer and connect the charger object:

    >>> fobj = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
    >>> pipe = pipecat.device.charger.icharger208b(fobj)

    Retrieve records from the charger during charging:

    >>> for record in pipe:
    ...   print record

    Parameters
    ----------
    fobj: file-like object, typically an instance of :class:`serial.Stream`

    Yields
    ------
    records: dict
        Records will contain information including the charge mode, supply
        voltage, battery voltage, battery current, internal and external
        charger temperature, and the total charged added-to / removed-from the
        battery.
    """

    modes = {
        1: "charge",
        2: "discharge",
        3: "monitor",
        4: "wait",
        5: "motor",
        6: "finished",
        7: "error",
        8: "trickle-LIxx",
        9: "trickle-NIxx",
        10: "foam-cut",
        11: "info",
        12: "discharge-external",
    }

    for record in source:
        raw = record["string"].strip().split(";")

        record = dict()
        add_field(record, ("charger", "mode"), modes[int(raw[1])])
        add_field(record, ("charger", "supply"), quantity(float(raw[3]) / 1000, units.volts))
        add_field(record, ("battery", "voltage"), quantity(float(raw[4]) / 1000, units.volts))
        add_field(record, ("battery", "current"), quantity(float(raw[5]) * 10, units.milliamps))
        add_field(record, ("charger", "temperature", "internal"), quantity(float(raw[14]) / 10, units.degC))
        add_field(record, ("charger", "temperature", "external"), quantity(float(raw[15]) / 10, units.degC))
        add_field(record, ("battery", "charge"), quantity(float(raw[16]), units.milliamps * units.hours))

        yield record
