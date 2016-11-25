__version__ = "0.1.0-dev"

import logging

import arrow
import pint

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

units = pint.UnitRegistry()
quantity = units.Quantity

def store(observation, key, value):
    observation[key] = value

def pprint(observation):
    for key in sorted(observation.keys()):
        print "%s: %s" % (key, observation[key])
    print
