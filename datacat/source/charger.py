# Copyright 2016 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data sources that retrieve information from battery chargers."""

from __future__ import absolute_import, division, print_function

from datacat import quantity, units
from datacat.record import add_field

def icharger208b(fobj):
    """Read data from an iCharger 208B battery charger.

    Logs data events emitted by the charger during charge, discharge, etc.

    Parameters
    ----------
    fobj: file-like object, typically an instance of serial.Stream
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

    for line in fobj:
        raw = line.strip().split(";")

        record = dict()
        add_field(record, ("charger", "mode"), modes[int(raw[1])])
        add_field(record, ("charger", "supply"), quantity(float(raw[3]) / 1000, units.volts))
        add_field(record, ("battery", "voltage"), quantity(float(raw[4]) / 1000, units.volts))
        add_field(record, ("battery", "current"), quantity(float(raw[5]) * 10, units.milliamps))
        add_field(record, ("charger", "temperature", "internal"), quantity(float(raw[14]) / 10, units.degC))
        add_field(record, ("charger", "temperature", "external"), quantity(float(raw[15]) / 10, units.degC))
        add_field(record, ("battery", "charge"), quantity(float(raw[16]), units.milliamps * units.hours))

        yield record
