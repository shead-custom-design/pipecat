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

"""Data sources that decode weather information."""

from __future__ import absolute_import, division, print_function

import arrow

from pipecat import quantity, units
from pipecat.record import add_field


def metars(source, key="xml"):
    """Parse METAR information retrieved from https://aviationweather.gov/metar.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>` returning records containing XML data, required
    key: :ref:`Record key <record-keys>`, optional

    Yields
    ------
    record: dict
        Records will contain METAR data extracted from XML.
    """

    for record in source:
        response = record[key]
        for data in response.findall("data"):
            for metar in sorted(data.findall("METAR"), key=lambda x: x.find("observation_time").text):
                output = dict()
                for element in metar.findall("raw_text"):
                    add_field(output, "raw", element.text)
                for element in metar.findall("station_id"):
                    add_field(output, "station-id", element.text)
                for element in metar.findall("observation_time"):
                    add_field(output, "observation-time", arrow.get(element.text))
                for element in metar.findall("latitude"):
                    add_field(output, "latitude", quantity(float(element.text), units.degrees))
                for element in metar.findall("longitude"):
                    add_field(output, "longitude", quantity(float(element.text), units.degrees))
                for element in metar.findall("temp_c"):
                    add_field(output, "temperature", quantity(float(element.text), units.degC))
                for element in metar.findall("depoint_c"):
                    add_field(output, "dewpoint", quantity(float(element.text), units.degC))
                for element in metar.findall("wind_dir_degrees"):
                    add_field(output, "wind-direction", quantity(float(element.text), units.degrees))
                for element in metar.findall("wind_speed_kt"):
                    add_field(output, "wind-speed", quantity(float(element.text), units.nautical_miles_per_hour))
                for element in metar.findall("visibility_statute_mi"):
                    add_field(output, "visibility", quantity(float(element.text), units.mile))
                for element in metar.findall("altim_in_hg"):
                    add_field(output, "altimeter", quantity(float(element.text), units.inHg))
                for element in metar.findall("flight_category"):
                    add_field(output, "flight-category", element.text)
                for element in metar.findall("elevation_m"):
                    add_field(output, "elevation", quantity(float(element.text), units.meters))
                yield output
