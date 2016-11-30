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

import itertools
import threading
import Queue

import datacat


def add(source, key, value):
    """Adds a key-value pair to every record returned from another source."""
    for record in source:
        datacat.store(record, key, value)
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
        thread = threading.Thread(target=send_to_queue, args=(source, queue))
        thread.start()
        consumers.append(receive_from_queue(queue))
    return concatenate(consumers)


def receive_from_queue(queue):
    """Receive records from a queue."""
    while True:
        record = queue.get()
        if record is StopIteration:
            break
        yield record

def send_to_queue(source, queue):
    """Send records from a source to a queue."""
    for record in source:
        queue.put(record)
    queue.put(StopIteration)


def trace(source):
    for record in source:
        datacat.log.debug(record)
        yield record

