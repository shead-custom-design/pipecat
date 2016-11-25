from datacat import arrow, store, quantity, units

import copy
import time

def timestamp(source, key="timestamp"):
    for observation in source:
        store(observation, key, arrow.utcnow())
        yield observation

def metronome(rate=quantity(1.0, units.seconds), prototype={}):
    while True:
        yield copy.deepcopy(prototype)
        time.sleep(rate.to(units.seconds).magnitude)
