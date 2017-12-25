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


def parse(source, key="string", keyout="json"):
    """Parse JSON data from records.

    This filter parses an incoming record key as JSON, appending the JSON data
    to the output.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, optional
        The key in incoming records to parse as JSON.
    keyout: :ref:`Record key <record-keys>`, optional
        The key in outgoing records where the parsed JSON will be stored.

    Yields
    ------
    record: dict
        Input records with an additional `keyout` field containing JSON-compatible data.
    """
    for record in source:
        try:
            pipecat.record.add_field(record, keyout, json.loads(record[key]))
            yield record
        except Exception as e:
            log.error(e)
