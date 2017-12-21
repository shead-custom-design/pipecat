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

"""Functions for working with JSON data.
"""

from __future__ import absolute_import, division, print_function

import json
import logging

import pipecat.record

log = logging.getLogger(__name__)


def parse(source, key="string", delimiter="/"):
    """Parse JSON data from a record.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, optional

    Yields
    ------
    records: dict
        Top-level key-value pairs in the JSON will become record fields.
    """
    for record in source:
        try:
            data = json.loads(record[key])

            output = {}
            for k, v in data.items():

                if delimiter:
                    k = k.split(delimiter)
                    k = tuple(k) if len(k) > 1 else k[0]

                    if isinstance(v, dict) and "value" in v and "units" in v:
                        v = pipecat.quantity(v["value"], v["units"])

                pipecat.record.add_field(output, k, v)
            yield output
        except Exception as e:
            log.error(e)
