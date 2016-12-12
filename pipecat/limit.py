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

"""Functions to limit the output of a Pipecat pipeline."""

from __future__ import absolute_import, division, print_function

import itertools
import threading
import time

import pipecat.queue


def count(source, count, name=None): # pylint: disable=redefined-outer-name
    """Limits the number of records returned from a source.

    Examples
    --------

    Produce seven records at one-second intervals:

    >>> pipe = pipecat.device.clock.metronome()
    >>> pipe = pipecat.limit.count(pipe, count=7)
    >>> for record in pipe:
    ...     print record

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    count: int, required
        The number of records that will be returned from `source`.
    name: string, optional.
        Optional name for this :ref:`Record generator <record-generators>` to
        use in log output.  Defaults to the function name.
    """
    if name is None:
        name = source.__name__

    for index in itertools.count():
        if index + 1 > count:
            pipecat.log.debug("%s iteration stopped after %s records.", name, count)
            break
        yield next(source)


def duration(source, duration, timeout=pipecat.quantity(0.1, pipecat.units.seconds), name=None): # pylint: disable=redefined-outer-name
    """Return records from a source until a fixed time duration has expired.

    Examples
    --------

    Produce records at one-second intervals for three minutes:

    >>> pipe = pipecat.device.clock.metronome()
    >>> pipe = pipecat.limit.duration(pipe, pipecat.quantity(3, pipecat.units.minutes))
    >>> for record in pipe:
    ...     print record

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    duration: time quantity, required
        Maximum amount of time that records will be returned from `source`.
    timeout: time quantity, optional.
        Limits the amount of time to block while waiting for output from
        `source`.  This affects the accuracy of when the function exits.
    name: string, optional.
        Optional name for this :ref:`Record generator <record-generators>` to
        use in log output.  Defaults to the function name.
    """
    if name is None:
        name = source.__name__

    end_time = time.time() + duration.to(pipecat.units.seconds).magnitude
    queue_timeout = timeout.to(pipecat.units.seconds).magnitude

    queue = pipecat.queue.Queue()
    shutdown = threading.Event()
    thread = threading.Thread(target=pipecat.queue.send, args=(source, queue, shutdown))
    thread.start()

    while True:
        if time.time() >= end_time:
            pipecat.log.debug("%s iteration stopped after %s time limit.", name, duration)
            shutdown.set()
            break
        try:
            record = queue.get(block=True, timeout=queue_timeout)
        except pipecat.queue.Empty:
            continue
        if record is StopIteration:
            break
        yield record


def timeout(source, timeout, initial=pipecat.quantity(1, pipecat.units.hours), name=None): # pylint: disable=redefined-outer-name
    """Return records from another source until they stop arriving.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    timeout: time quantity, required
        Maximum time to wait for the next record before exiting.
    initial: time quantity, optional
        Maximum time to wait for the first record.
    name: string, optional.
        Optional name for this :ref:`Record generator <record-generators>` to
        use in log output.  Defaults to the function name.
    """
    if name is None:
        name = source.__name__

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
            pipecat.log.debug("%s iteration stopped by %s timeout.", name, timeout)
            shutdown.set()
            break
        if record is StopIteration:
            break
        yield record

def until(source, key, value, name=None):
    """Return records from another source until a record occurs with a specific key and value.

    Examples
    --------

    Print output from a battery charger until its mode changes to "finished":

    >>> pipe = <battery charger pipeline>
    >>> pipe = pipecat.limit.until(pipe, "mode", "finished")
    >>> for record in pipe:
    ...     print record

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    key: :ref:`Record key <record-keys>`, required
    value: anything, required
    name: string, optional.
        Optional name for this :ref:`Record generator <record-generators>` to
        use in log output.  Defaults to the function name.
    """
    if name is None:
        name = source.__name__
    for record in source:
        yield record
        if key in record and record[key] == value:
            pipecat.log.debug("%s iteration stopped because record contained %s == %r", name, key, value)
            break

