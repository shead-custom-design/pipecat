Feature: Utility

    Scenario: pipecat.utility.readline
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And after iterating through the pipe contents.
        Then 1390 records will be returned.
        And every record will contain a "string" key with a bytes value.

    Scenario: pipecat.utility.add_timestamp
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.utility.add_timestamp.
        And after iterating through the pipe contents.
        Then every record will contain a "string" key with a bytes value.
        And every record will contain a "timestamp" key with an arrow value.
