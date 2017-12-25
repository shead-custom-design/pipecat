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

"""Functions for working with queues."""

from __future__ import absolute_import, division, print_function

# For portability between Python 2 and 3
try:
    from Queue import Queue, Empty # pylint: disable=import-error,unused-import
except ImportError:
    from queue import Queue, Empty # pylint: disable=import-error,unused-import


def receive(queue):
    """Receive records from a queue.

    Queues are a handy mechanism for passing data between threads.  Use this
    function to receive records sent over a queue by :func:`pipecat.queue.send`.

    Parameters
    ----------
    queue: :class:`queue.Queue`, required

    Yields
    ------
    record: dict
    """
    while True:
        record = queue.get()
        if record is StopIteration:
            break
        yield record


def send(source, queue, shutdown=None):
    """Send records from a source to a queue.

    Queues are a handy mechanism for passing data between threads.  Use this
    function to send records over a queue to :func:`pipecat.queue.receive`.

    Parameters
    ----------
    source: :ref:`Record generator <record-generators>`, required
    queue: :class:`queue.Queue`, required
    shutdown: :class:`threading.Event`, optional.
        If supplied, callers can set the event to safely stop sending from another thread.
    """
    for record in source:
        queue.put(record)
        if shutdown and shutdown.isSet():
            return
    queue.put(StopIteration)
