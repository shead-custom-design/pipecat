"""Data sources that retrieve information from battery chargers."""

from __future__ import absolute_import, division, print_function

from datacat import store, quantity, units

def icharger208b(stream):
    """Read data from an iCharger 208B battery charger.

    Logs data events emitted by the charger during charge, discharge, etc.

    Parameters
    ----------
    stream: file-like object, typically an instance of serial.Stream
    """

    modes = {
        1: "charge",
        2: "discharge",
        3: "monitor",
        4: "wait",
        5: "motor",
        6: "finished",
        7: "error",
        8: "trickle-LIxx",
        9: "trickle-NIxx",
        10: "foam-cut",
        11: "info",
        12: "discharge-external",
    }

    for line in stream:
        raw = line.strip().split(";")

        record = dict()
        store(record, ("charger", "mode"), modes[int(raw[1])])
        store(record, ("charger", "supply"), quantity(float(raw[3]) / 1000, units.volts))
        store(record, ("battery", "voltage"), quantity(float(raw[4]) / 1000, units.volts))
        store(record, ("battery", "current"), quantity(float(raw[5]) * 10, units.milliamps))
        store(record, ("charger", "temperature", "internal"), quantity(float(raw[14]) / 10, units.degC))
        store(record, ("charger", "temperature", "external"), quantity(float(raw[15]) / 10, units.degC))
        store(record, ("battery", "charge"), quantity(float(raw[16]), units.milliamps * units.hours))

        yield record
