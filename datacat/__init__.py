from __future__ import absolute_import, division, print_function

__version__ = "0.1.0-dev"

import logging
import sys

import pint

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

units = pint.UnitRegistry()
quantity = units.Quantity

def store(observation, key, value):
    if key in observation:
        log.warning("Overwriting %s=%s with %s=%s", key, observation[key], key, value)
    observation[key] = value

def dump(observation, stream=sys.stdout):
    for key, value in sorted(observation.items()):
        if isinstance(key, tuple):
            key = "/".join(key)
        stream.write("%s: %s\n" % (key, value))
    stream.write("\n")
