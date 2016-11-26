"""Data sources from which information can be logged."""

from __future__ import absolute_import, division, print_function

import itertools
import threading
import Queue

import datacat


def add(source, key, value):
    """Adds a key-value pair to every observation returned from another source."""
    for observation in source:
        datacat.store(observation, key, value)
        yield observation


def limit(source, count):
    """Limits the number of observations returned from another source."""
    for index, observation in enumerate(source):
        if index >= count:
            datacat.log.info("Stopped by %s observation limit." % count)
            break
        yield observation


def send_to_queue(source, queue):
    """Send observations from a source to a queue."""
    for observation in source:
        queue.put(observation)
    queue.put(StopIteration)


def receive_from_queue(queue):
    """Receive observations from a queue."""
    while True:
        observation = queue.get()
        if observation is StopIteration:
            break
        yield observation


def concatenate(sources):
    """Concatenate observations from multiple sources."""
    for source in sources:
        for observation in source:
            yield observation


def multiplex(*sources):
    """Interleave observations from multiple sources."""
    queue = Queue.Queue()
    consumers = []
    for source in sources:
        thread = threading.Thread(target=send_to_queue, args=(source, queue))
        thread.start()
        consumers.append(receive_from_queue(queue))
    return concatenate(consumers)

