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

"""Functions for working with XML data.
"""

from __future__ import absolute_import, division, print_function

import logging
import xml.etree.ElementTree as xml

import pipecat.record

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def parse(source, key="string"):
    """Parse XML data from a record.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, optional

    Yields
    ------
    records: dict
        Each record will contain a single `xml` key containing an XML DOM parsed from a source record.
    """
    for record in source:
        try:
            output = {}
            pipecat.record.add_field(output, "xml", xml.fromstring(record[key]))
            yield output
        except Exception as e:
            log.error(e)
