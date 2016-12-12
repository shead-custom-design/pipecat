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

"""Functions for connecting data sources."""

from __future__ import absolute_import, division, print_function

import threading

import pipecat.queue


def concatenate(sources):
    """Concatenate records from multiple sources.

    Yields all of the records from the first source, then all the records from
    the second source, and-so-on until every source has been consumed.  Note that
    this means that it only makes sense to use sources that return a bounded
    number of records with `concatenate()`!

    Parameters
    ----------
    sources: sequence of :ref:`record-generators`, required

    Yields
    ------
    records: dict
        Returns records from each source in-turn.
    """
    for source in sources:
        for record in source:
            yield record


def multiplex(sources):
    """Interleave records from multiple sources.

    Parameters
    ----------
    sources: sequence of :ref:`record-generators`, required

    Yields
    ------
    records: dict
        Returns records from all sources as they arrive.
    """
    queue = pipecat.queue.Queue()
    consumers = []
    for source in sources:
        thread = threading.Thread(target=pipecat.queue.send, args=(source, queue))
        thread.start()
        consumers.append(pipecat.queue.receive(queue))
    return concatenate(consumers)


