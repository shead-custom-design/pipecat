Feature: pipecat.record

    Scenario: pipecat.record.dump
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.device.charger.icharger208b
        And an instance of pipecat.limit.count set to 1
        And a string stream.
        When iterating through the pipe contents.
        Then records can be dumped to the stream.
        And the stream contents will match pipecat-record-dump.txt
