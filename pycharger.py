#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
########################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

import serial

# iCharger modes of operation
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

ser = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
ser.isOpen()

### MAIN #############################################################

while 1 :
    line = ser.readline()
    raw = line.split(";")

    mode = modes[int(raw[1])]
    supply_voltage = float(raw[3]) / 1000
    battery_voltage = float(raw[4]) / 1000
    charge_current = int(raw[5]) * 10
#    v_c1 = float (raw[6])/1000
#    v_c2 = float (raw[7])/1000
#    v_c3 = float (raw[8])/1000
    internal_temperature = float(raw[14]) / 10
    external_temperature = float(raw[15]) / 10
    charge_amount = float(raw[16]) / 1000


    print line.strip()
    print "Mode: %s" % mode
    print "Supply: %s V" % supply_voltage
    print "Batt: %s V" % battery_voltage
#    print "Cell 1: " + str(v_c1) + " V (" + str(s_vc1) + "%)"
#    print "Cell 2: " + str(v_c2) + " V (" + str(s_vc2) + "%)"
#    print "Cell 3: " + str(v_c3) + " V (" + str(s_vc3) + "%)"
    print "Charge Current: %s mA" % charge_current
    print "Charge Amount: %s mA" % charge_amount
    print "Temp INT: %s °C" % internal_temperature
    print "Temp EXT: %s °C" % external_temperature

    print
