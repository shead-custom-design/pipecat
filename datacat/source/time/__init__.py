import time

import arrow

import datacat

def timestamp(source, key="timestamp"):
    for observation in source:
        datacat.store(observation, key, arrow.utcnow())
        yield observation

def metronome(rate=datacat.quantity(1.0, datacat.units.seconds)):
    while True:
        yield dict()
        time.sleep(rate.to(datacat.units.seconds).magnitude)

