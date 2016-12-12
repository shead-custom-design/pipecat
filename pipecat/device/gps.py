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

"""Functions for working with GPS receivers.
"""

from __future__ import absolute_import, division, print_function

import functools
import operator

import pipecat.record

def nmea(source):
    """Parse NMEA messages from raw strings.

    Examples
    --------

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>` returning records containing a "string" field.

    Yields
    ------
    records: dict
        Records will contain varying amounts of time, position, speed, heading,
        pitch, roll, and quality information based on device sending the data.
        Support is provided for GPGGA, GPGLL, GPRMC, GPTXT, HCHDG, and PASHR
        messages.
    """
    def latitude(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "N" else -1.0) * (float(degrees[:2]) + (float(degrees[2:]) / 60.0))
        return pipecat.quantity(degrees, pipecat.units.degrees)

    def longitude(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "E" else -1.0) * (float(degrees[:3]) + (float(degrees[3:]) / 60.0))
        return pipecat.quantity(degrees, pipecat.units.degrees)

    def variation(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "E" else -1.0) * float(degrees)
        return pipecat.quantity(degrees, pipecat.units.degrees)

    for record in source:
        sentence = record.get("string", "")
        if sentence[0] != "$":
            pipecat.log.warning("Not a valid NMEA sentence.")
            continue
        sentence = sentence[1:].strip()
        sentence, checksum = sentence.split("*", 1)
        checksum = int(checksum, 16)
        calculated_checksum = functools.reduce(operator.xor, (ord(s) for s in sentence), 0)
        if checksum != calculated_checksum:
            pipecat.log.warning("NMEA sentence failed checksum.")
            continue

        sentence = sentence.split(",")

        record = {}
        pipecat.record.add_field(record, "id", sentence[0])

        if sentence[0] == "GPGGA":
            pipecat.record.add_field(record, "time", sentence[1])
            pipecat.record.add_field(record, "latitude", latitude(sentence[2], sentence[3]))
            pipecat.record.add_field(record, "longitude", longitude(sentence[4], sentence[5]))
            pipecat.record.add_field(record, "quality", int(sentence[6]))
            pipecat.record.add_field(record, "satellites", int(sentence[7]))
            pipecat.record.add_field(record, "dop", float(sentence[8]))
            pipecat.record.add_field(record, "altitude", pipecat.quantity(float(sentence[9]), pipecat.units.meters))
            pipecat.record.add_field(record, "geoid-height", pipecat.quantity(float(sentence[11]), pipecat.units.meters))
        elif sentence[0] == "GPGLL":
            pipecat.record.add_field(record, "latitude", latitude(sentence[1], sentence[2]))
            pipecat.record.add_field(record, "longitude", longitude(sentence[3], sentence[4]))
            pipecat.record.add_field(record, "time", sentence[5])
            pipecat.record.add_field(record, "active", sentence[6] == "A")
        elif sentence[0] == "GPRMC":
            pipecat.record.add_field(record, "time", sentence[1])
            pipecat.record.add_field(record, "active", sentence[2] == "A")
            pipecat.record.add_field(record, "latitude", latitude(sentence[3], sentence[4]))
            pipecat.record.add_field(record, "longitude", longitude(sentence[5], sentence[6]))
            pipecat.record.add_field(record, "speed", pipecat.quantity(float(sentence[7]), pipecat.units.knots))
            pipecat.record.add_field(record, "track", pipecat.quantity(float(sentence[8]), pipecat.units.degrees))
            pipecat.record.add_field(record, "date", sentence[9])
            pipecat.record.add_field(record, "variation", variation(sentence[10], sentence[11]))
        elif sentence[0] == "GPTXT":
            pipecat.record.add_field(record, "text", sentence[4])
        elif sentence[0] == "HCHDG":
            pipecat.record.add_field(record, "heading", pipecat.quantity(float(sentence[1]), pipecat.units.degree))
            pipecat.record.add_field(record, "variation", variation(sentence[4], sentence[5]))
        elif sentence[0] == "PASHR":
            pipecat.record.add_field(record, "time", sentence[1])
            pipecat.record.add_field(record, "heading", pipecat.quantity(float(sentence[2]), pipecat.units.degree))
            pipecat.record.add_field(record, "roll", pipecat.quantity(float(sentence[4]), pipecat.units.degree))
            pipecat.record.add_field(record, "pitch", pipecat.quantity(float(sentence[5]), pipecat.units.degree))
            pipecat.record.add_field(record, "heave", pipecat.quantity(float(sentence[6]), pipecat.units.meters))
            pipecat.record.add_field(record, "roll-accuracy", pipecat.quantity(float(sentence[7]), pipecat.units.degrees))
            pipecat.record.add_field(record, "pitch-accuracy", pipecat.quantity(float(sentence[8]), pipecat.units.degrees))
            pipecat.record.add_field(record, "heading-accuracy", pipecat.quantity(float(sentence[9]), pipecat.units.degrees))

        yield record
