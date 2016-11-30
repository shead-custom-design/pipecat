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

"""Options to constrain the information that is logged."""

from __future__ import absolute_import, division, print_function

import itertools
import threading
import time
import Queue

import datacat


def count(source, count): # pylint: disable=redefined-outer-name
    """Limits the number of records returned from another source."""
    for index in itertools.count():
        if index + 1 > count:
            datacat.log.info("Iteration stopped after %s records.", count)
            break
        yield next(source)


def duration(source, duration, timeout=datacat.quantity(0.1, datacat.units.seconds)): # pylint: disable=redefined-outer-name
    """Return records from another source until a fixed time duration has expired."""
    end_time = time.time() + duration.to(datacat.units.seconds).magnitude
    queue_timeout = timeout.to(datacat.units.seconds).magnitude

    queue = Queue.Queue()
    thread = threading.Thread(target=datacat.source.send_to_queue, args=(source, queue))
    thread.start()

    while True:
        if time.time() >= end_time:
            datacat.log.info("Iteration stopped after %s time limit.", duration)
            break
        try:
            record = queue.get(block=True, timeout=queue_timeout)
        except Queue.Empty:
            continue
        if record is StopIteration:
            break
        yield record


def timeout(source, timeout=datacat.quantity(5, datacat.units.seconds)): # pylint: disable=redefined-outer-name
    """Return records from another source until they stop arriving."""
    queue_timeout = timeout.to(datacat.units.seconds).magnitude

    queue = Queue.Queue()
    thread = threading.Thread(target=datacat.source.send_to_queue, args=(source, queue))
    thread.start()

    while True:
        try:
            record = queue.get(block=True, timeout=queue_timeout)
        except Queue.Empty:
            datacat.log.info("Iteration stopped by %s timeout.", timeout)
            break
        if record is StopIteration:
            break
        yield record

