Feature: pipecat.device.charger

    Scenario:
        Given an icharger 208b connected to a serial port.
        And a pyserial connection.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.device.charger.icharger208b
        And after iterating through the pipe contents.
        Then every record will contain a ("charger","mode") key with a string value.

#battery/cell1/voltage: 0.0 volt
#battery/cell2/voltage: 0.0 volt
#battery/cell3/voltage: 0.0 volt
#battery/cell4/voltage: 0.0 volt
#battery/cell5/voltage: 0.0 volt
#battery/cell6/voltage: 0.0 volt
#battery/cell7/voltage: 0.0 volt
#battery/cell8/voltage: 0.0 volt
#battery/charge: 0.0 hour * milliampere
#battery/current: 930.0 milliampere
#battery/voltage: 3.874 volt
#charger/mode: charge
#charger/supply: 12.25 volt
#charger/temperature/external: 23.6 degC
#charger/temperature/internal: 29.1 degC


