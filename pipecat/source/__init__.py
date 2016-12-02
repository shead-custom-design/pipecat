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

"""Data sources from which information can be logged."""

from __future__ import absolute_import, division, print_function

import threading
import Queue

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
    queue = Queue.Queue()
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

