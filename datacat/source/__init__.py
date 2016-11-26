"""Data sources from which information can be logged."""

from __future__ import absolute_import, division, print_function

import itertools
import threading
import Queue

import datacat

def add(source, key, value):
    for observation in source:
        datacat.store(observation, key, value)
        yield observation

def limit(source, count):
    for observation in itertools.islice(source, count):
        yield observation

def send_to_queue(source, queue):
    for observation in source:
        queue.put(observation)
    queue.put(StopIteration)

def receive_from_queue(queue):
    while True:
        observation = queue.get()
        if observation is StopIteration:
            break
        yield observation

def concatenate(sources):
    for source in sources:
        for observation in source:
            yield observation

def multiplex(*sources):
    queue = Queue.Queue()
    consumers = []
    for source in sources:
        thread = threading.Thread(target=send_to_queue, args=(source, queue))
        thread.start()
        consumers.append(receive_from_queue(queue))
    return concatenate(consumers)

