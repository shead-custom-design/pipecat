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

