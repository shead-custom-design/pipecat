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

"""Data sources that provide information related to time."""

from __future__ import absolute_import, division, print_function

import time

import arrow

import datacat.record

def timestamp(source, key="timestamp"):
    """Add a timestamp to every record returned from another source."""
    for record in source:
        datacat.record.add_field(record, key, arrow.utcnow())
        yield record


def metronome(rate=datacat.quantity(1.0, datacat.units.seconds)):
    """Generate an empty record at fixed time intervals."""
    while True:
        yield dict()
        time.sleep(rate.to(datacat.units.seconds).magnitude)


