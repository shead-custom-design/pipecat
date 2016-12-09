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

"""Functions to limit the output of a logging pipeline."""

from __future__ import absolute_import, division, print_function

import itertools
import threading
import time

import pipecat.queue


def count(source, count): # pylint: disable=redefined-outer-name
    """Limits the number of records returned from another source."""
    for index in itertools.count():
        if index + 1 > count:
            pipecat.log.info("Iteration stopped after %s records.", count)
            break
        yield next(source)


def duration(source, duration, timeout=pipecat.quantity(0.1, pipecat.units.seconds)): # pylint: disable=redefined-outer-name
    """Return records from another source until a fixed time duration has expired."""
    end_time = time.time() + duration.to(pipecat.units.seconds).magnitude
    queue_timeout = timeout.to(pipecat.units.seconds).magnitude

    queue = pipecat.queue.Queue()
    shutdown = threading.Event()
    thread = threading.Thread(target=pipecat.queue.send, args=(source, queue, shutdown))
    thread.start()

    while True:
        if time.time() >= end_time:
            pipecat.log.info("Iteration stopped after %s time limit.", duration)
            shutdown.set()
            break
        try:
            record = queue.get(block=True, timeout=queue_timeout)
        except pipecat.queue.Empty:
            continue
        if record is StopIteration:
            break
        yield record


def timeout(source, timeout, initial=pipecat.quantity(1, pipecat.units.hours)): # pylint: disable=redefined-outer-name
    """Return records from another source until they stop arriving.

    Parameters
    ----------
    source: generator, required
        A source of records.
    timeout: quantity, required
        Maximum time to wait for the next record.
    initial: quantity, optional
        Maximum time to wait for the first record.
    """
    initial_timeout = initial.to(pipecat.units.seconds).magnitude
    regular_timeout = timeout.to(pipecat.units.seconds).magnitude
    current_timeout = initial_timeout

    queue = pipecat.queue.Queue()
    shutdown = threading.Event()
    thread = threading.Thread(target=pipecat.queue.send, args=(source, queue, shutdown))
    thread.start()

    while True:
        try:
            record = queue.get(block=True, timeout=current_timeout)
            current_timeout = regular_timeout
        except pipecat.queue.Empty:
            pipecat.log.info("Iteration stopped by %s timeout.", timeout)
            shutdown.set()
            break
        if record is StopIteration:
            break
        yield record

def until(source, key, value):
    for record in source:
        yield record
        if key in record and record[key] == value:
            break

