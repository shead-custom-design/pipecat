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

"""Communication with Queue.Queue."""

from __future__ import absolute_import, division, print_function

# For portability between Python 2 and 3
try:
    from Queue import Queue, Empty # pylint: disable=unused-import,import-error
except ImportError:
    from queue import Queue, Empty # pylint: disable=unused-import,import-error

def receive(queue):
    """Receive records from a queue."""
    while True:
        record = queue.get()
        if record is StopIteration:
            break
        yield record

def send(source, queue):
    """Send records from a source to a queue."""
    for record in source:
        queue.put(record)
    queue.put(StopIteration)

