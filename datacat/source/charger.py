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
        1: "Charging",
        2: "Discharging",
        3: "Monitor",
        4: "Waiting",
        5: "Motor burn-in",
        6: "Finished",
        7: "Error",
        8: "LIxx trickle",
        9: "NIxx trickle",
        10: "Foam cut",
        11: "Info",
        12: "External-discharging",
    }

    for line in stream:
        raw = line.strip().split(";")

        observation = dict()
        store(observation, ("charger", "mode"), modes[int(raw[1])])
        store(observation, ("charger", "supply"), quantity(float(raw[3]) / 1000, units.volts))
        store(observation, ("battery", "voltage"), quantity(float(raw[4]) / 1000, units.volts))
        store(observation, ("battery", "current"), quantity(float(raw[5]) * 10, units.milliamps))
        store(observation, ("charger", "temperature", "internal"), quantity(float(raw[14]) / 10, units.degC))
        store(observation, ("charger", "temperature", "external"), quantity(float(raw[15]) / 10, units.degC))
        store(observation, ("battery", "charge"), quantity(float(raw[16]), units.milliamps * units.hours))

        yield observation
