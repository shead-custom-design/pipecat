Feature: pipecat.device.charger

    Scenario:
        Given an icharger 208b connected to a serial port.
        And a pyserial connection.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.device.charger.icharger208b
        When iterating through the pipe contents.
        Then every record will contain a ("charger","mode") key with a string value.

