from datacat import store, quantity, units

def icharger208b(stream):
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
        store(observation, "mode", modes[int(raw[1])])
        store(observation, "supply-voltage", quantity(float(raw[3]) / 1000, units.volts))
        store(observation, "battery-voltage", quantity(float(raw[4]) / 1000, units.volts))
        store(observation, "charge-current", quantity(float(raw[5]) * 10, units.milliamps))
        store(observation, "internal-temperature", quantity(float(raw[14]) / 10, units.degC))
        store(observation, "external-temperature", quantity(float(raw[15]) / 10, units.degC))
        store(observation, "charge-amount", quantity(float(raw[16]), units.milliamps * units.hours))

        yield observation
