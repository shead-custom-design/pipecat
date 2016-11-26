"""Data sources that provide information related to time."""

from __future__ import absolute_import, division, print_function

import threading
import time
import Queue

import arrow

import datacat

def timestamp(source, key="timestamp"):
    """Add a timestamp to every observation returned from another source."""
    for observation in source:
        datacat.store(observation, key, arrow.utcnow())
        yield observation


def metronome(rate=datacat.quantity(1.0, datacat.units.seconds)):
    """Generate an empty observation at fixed time intervals."""
    while True:
        yield dict()
        time.sleep(rate.to(datacat.units.seconds).magnitude)


def limit(source, duration, timeout=datacat.quantity(0.1, datacat.units.seconds)):
    """Return observations from another source until a fixed time duration has expired."""
    end_time = time.time() + duration.to(datacat.units.seconds).magnitude
    queue_timeout = timeout.to(datacat.units.seconds).magnitude

    queue = Queue.Queue()
    thread = threading.Thread(target=datacat.source.send_to_queue, args=(source, queue))
    thread.start()

    while True:
        if time.time() >= end_time:
            datacat.log.info("Stopped by %s time limit." % duration)
            break
        try:
            observation = queue.get(block=True, timeout=queue_timeout)
        except Queue.Empty:
            continue
        if observation is StopIteration:
            break
        yield observation


def timeout(source, timeout=datacat.quantity(5, datacat.units.seconds)):
    """Return observations from another source until they stop arriving."""
    queue_timeout = timeout.to(datacat.units.seconds).magnitude

    queue = Queue.Queue()
    thread = threading.Thread(target=datacat.source.send_to_queue, args=(source, queue))
    thread.start()

    while True:
        try:
            observation = queue.get(block=True, timeout=queue_timeout)
        except Queue.Empty:
            datacat.log.info("Stopped by %s timeout." % timeout)
            break
        if observation is StopIteration:
            break
        yield observation

