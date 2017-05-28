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
    records: dict
        Records will contain METAR data extracted from XML.
    """

    for record in source:
        response = record[key]
        for data in response.findall("data"):
            for metar in sorted(data.findall("METAR"), key=lambda x: x.find("observation_time").text):
                output = dict()
                add_field(output, "raw", metar.find("raw_text").text)
                add_field(output, "station-id", metar.find("station_id").text)
                add_field(output, "observation-time", arrow.get(metar.find("observation_time").text))
                add_field(output, "latitude", quantity(float(metar.find("latitude").text), units.degrees))
                add_field(output, "longitude", quantity(float(metar.find("longitude").text), units.degrees))
                add_field(output, "temperature", quantity(float(metar.find("temp_c").text), units.degC))
                add_field(output, "dewpoint", quantity(float(metar.find("dewpoint_c").text), units.degC))
                add_field(output, "wind-direction", quantity(float(metar.find("wind_dir_degrees").text), units.degrees))
                add_field(output, "wind-speed", quantity(float(metar.find("wind_speed_kt").text), units.nautical_miles_per_hour))
                add_field(output, "visibility", quantity(float(metar.find("visibility_statute_mi").text), units.mile))
                add_field(output, "altimeter", quantity(float(metar.find("altim_in_hg").text), units.inHg))
                add_field(output, "flight-category", metar.find("flight_category").text)
                add_field(output, "elevation", quantity(float(metar.find("elevation_m").text), units.meters))
                yield output
