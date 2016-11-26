"""Data logging library."""

from __future__ import absolute_import, division, print_function

import logging
import sys

import pint

__version__ = "0.1.0-dev"

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

units = pint.UnitRegistry()
quantity = units.Quantity

def store(observation, key, value):
    """Add a key-value pair to an observation.

    Parameters
    ----------
    observation: dict, required
        Dictionary of key-value pairs that constitute an observation.
    key: string or tuple of strings, required
        Observation key to be overwritten.
    value: object
        New observation value.
    """

    if key in observation:
        log.warning("Overwriting %s=%s with %s=%s", key, observation[key], key, value)
    observation[key] = value

def dump(observation, stream=sys.stdout):
    """Dump a human-readable text representation of an observation to a stream.

    Parameters
    ----------
    observation: dict, required
        Dictionary of key-value pairs to be written-out.
    stream: file-like object, optional
    """

    for key, value in sorted(observation.items()):
        if isinstance(key, tuple):
            key = "/".join(key)
        stream.write("%s: %s\n" % (key, value))
    stream.write("\n")
