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

import pipecat.record

def nmea(source):
    """Parse NMEA messages from raw strings."""
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
        calculated_checksum = reduce(operator.xor, (ord(s) for s in sentence), 0)
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
