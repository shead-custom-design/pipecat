"""Data sources that provide information related to time."""

from __future__ import absolute_import, division, print_function

import time

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

