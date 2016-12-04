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

"""Data sources from which information can be logged."""

from __future__ import absolute_import, division, print_function

import threading

import pipecat.record
import pipecat.queue

def add(source, key, value):
    """Adds a key-value pair to every record returned from another source."""
    for record in source:
        pipecat.record.add_field(record, key, value)
        yield record


def concatenate(sources):
    """Concatenate records from multiple sources."""
    for source in sources:
        for record in source:
            yield record


def multiplex(*sources):
    """Interleave records from multiple sources."""
    queue = pipecat.queue.Queue()
    consumers = []
    for source in sources:
        thread = threading.Thread(target=pipecat.queue.send, args=(source, queue))
        thread.start()
        consumers.append(pipecat.queue.receive(queue))
    return concatenate(consumers)


def trace(source):
    """Log records for debugging."""
    for record in source:
        pipecat.log.debug(record)
        yield record

