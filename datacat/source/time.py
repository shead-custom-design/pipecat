"""Data sources that provide information related to time."""

from __future__ import absolute_import, division, print_function

import time

import arrow

import datacat

def timestamp(source, key="timestamp"):
    """Add a timestamp to every record returned from another source."""
    for record in source:
        datacat.store(record, key, arrow.utcnow())
        yield record


def metronome(rate=datacat.quantity(1.0, datacat.units.seconds)):
    """Generate an empty record at fixed time intervals."""
    while True:
        yield dict()
        time.sleep(rate.to(datacat.units.seconds).magnitude)


