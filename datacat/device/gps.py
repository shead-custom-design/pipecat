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

"""Functions for working with UDP messages.
"""

from __future__ import absolute_import, division, print_function

import operator

import arrow

import datacat.record

def nmea(source):
    def latitude(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "N" else -1.0) * (float(degrees[:2]) + (float(degrees[2:]) / 60.0))
        return datacat.quantity(degrees, datacat.units.degrees)

    def longitude(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "E" else -1.0) * (float(degrees[:3]) + (float(degrees[3:]) / 60.0))
        return datacat.quantity(degrees, datacat.units.degrees)

    def variation(degrees, hemisphere):
        degrees = (1.0 if hemisphere == "E" else -1.0) * float(degrees)
        return datacat.quantity(degrees, datacat.units.degrees)

    """Parse NMEA GPS data from raw strings."""
    for record in source:
        sentence = record.get("string", "")
        if sentence[0] != "$":
            datacat.log.warning("Not a valid NMEA sentence.")
            continue
        sentence = sentence[1:].strip()
        sentence, checksum = sentence.split("*", 1)
        checksum = int(checksum, 16)
        calculated_checksum = reduce(operator.xor, (ord(s) for s in sentence), 0)
        if checksum != calculated_checksum:
            datacat.log.warning("NMEA sentence failed checksum.")
            continue

        sentence = sentence.split(",")

        record = {}
        datacat.record.add_field(record, "id", sentence[0])

        if sentence[0] == "GPGGA":
            datacat.record.add_field(record, "time", sentence[1])
            datacat.record.add_field(record, "latitude", latitude(sentence[2], sentence[3]))
            datacat.record.add_field(record, "longitude", longitude(sentence[4], sentence[5]))
            datacat.record.add_field(record, "quality", int(sentence[6]))
            datacat.record.add_field(record, "satellites", int(sentence[7]))
            datacat.record.add_field(record, "dop", float(sentence[8]))
            datacat.record.add_field(record, "altitude", datacat.quantity(float(sentence[9]), datacat.units.meters))
            datacat.record.add_field(record, "geoid-height", datacat.quantity(float(sentence[11]), datacat.units.meters))
        elif sentence[0] == "GPGLL":
            datacat.record.add_field(record, "latitude", latitude(sentence[1], sentence[2]))
            datacat.record.add_field(record, "longitude", longitude(sentence[3], sentence[4]))
            datacat.record.add_field(record, "time", sentence[5])
            datacat.record.add_field(record, "active", sentence[6] == "A")
        elif sentence[0] == "GPRMC":
            datacat.record.add_field(record, "time", sentence[1])
            datacat.record.add_field(record, "active", sentence[2] == "A")
            datacat.record.add_field(record, "latitude", latitude(sentence[3], sentence[4]))
            datacat.record.add_field(record, "longitude", longitude(sentence[5], sentence[6]))
            datacat.record.add_field(record, "speed", datacat.quantity(float(sentence[7]), datacat.units.knots))
            datacat.record.add_field(record, "track", datacat.quantity(float(sentence[8]), datacat.units.degrees))
            datacat.record.add_field(record, "date", sentence[9])
            datacat.record.add_field(record, "variation", variation(sentence[10], sentence[11]))
        elif sentence[0] == "GPTXT":
            datacat.record.add_field(record, "text", sentence[4])
        elif sentence[0] == "HCHDG":
            datacat.record.add_field(record, "heading", datacat.quantity(float(sentence[1]), datacat.units.degree))
            datacat.record.add_field(record, "variation", variation(sentence[4], sentence[5]))
        elif sentence[0] == "PASHR":
            datacat.record.add_field(record, "time", sentence[1])
            datacat.record.add_field(record, "heading", datacat.quantity(float(sentence[2]), datacat.units.degree))
            datacat.record.add_field(record, "roll", datacat.quantity(float(sentence[4]), datacat.units.degree))
            datacat.record.add_field(record, "pitch", datacat.quantity(float(sentence[5]), datacat.units.degree))
            datacat.record.add_field(record, "heave", datacat.quantity(float(sentence[6]), datacat.units.meters))
            datacat.record.add_field(record, "roll-accuracy", datacat.quantity(float(sentence[7]), datacat.units.degrees))
            datacat.record.add_field(record, "pitch-accuracy", datacat.quantity(float(sentence[8]), datacat.units.degrees))
            datacat.record.add_field(record, "heading-accuracy", datacat.quantity(float(sentence[9]), datacat.units.degrees))

        yield record
