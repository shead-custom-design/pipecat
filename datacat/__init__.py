__version__ = "0.1.0-dev"

import arrow

import pint
units = pint.UnitRegistry()

def timestamp(source):
    for observation in source:
        observation["timestamp"] = arrow.utcnow()
        yield observation

def icharger(stream):
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

    while True:
        line = stream.readline()
        raw = line.split(";")

        observation = dict()
        observation["mode"] = modes[int(raw[1])]
        observation["supply-voltage"] = units.Quantity(float(raw[3]) / 1000, units.volts)
        observation["battery-voltage"] = units.Quantity(float(raw[4]) / 1000, units.volts)
        observation["charge-current"] = units.Quantity(float(raw[5]) * 10, units.milliamps)
#    v_c1 = float (raw[6])/1000
#    v_c2 = float (raw[7])/1000
#    v_c3 = float (raw[8])/1000
        observation["internal-temperature"] = units.Quantity(float(raw[14]) / 10, units.degC)
        observation["external-temperature"] = units.Quantity(float(raw[15]) / 10, units.degC)
        observation["charge-amount"] = units.Quantity(float(raw[16]), units.milliamps * units.hours)

        yield observation
