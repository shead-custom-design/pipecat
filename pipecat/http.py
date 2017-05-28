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

"""Functions for working with HTTP requests.
"""

from __future__ import absolute_import, division, print_function

import logging
import time

import requests

import pipecat.record

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get(*args, **kwargs):
    """Retrieve data using HTTP requests.

    Accepts the same parameters as :func:`requests.get`, plus the following:

    Parameters
    ----------
    poll: time quantity, optional.
        Time to wait between requests.

    Yields
    ------
    records: dict
        Records will contain a single `string` key with the contents returned from each request.
    """
    poll = kwargs.pop("poll", pipecat.quantity(5, pipecat.units.seconds)).to(pipecat.units.seconds).magnitude

    while True:
        try:
            result = requests.get(*args, **kwargs)

            record = {}
            pipecat.record.add_field(record, "status", result.status_code)
            for key, value in result.headers.items():
                pipecat.record.add_field(record, ("header", key), value)
            pipecat.record.add_field(record, "encoding", result.encoding)
            pipecat.record.add_field(record, "string", result.text)

            yield record
        except Exception as e:
            log.error(e)

        time.sleep(poll)
