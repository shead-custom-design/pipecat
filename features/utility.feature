Feature: Utility

    Scenario: pipecat.utility.readline
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        Then after iterating through the pipe's contents.
        Then 1390 records will be returned.
        And every record will contain a string key.
        And the string key will have a string value.

    Scenario: pipecat.utility.add_timestamp
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.utility.add_timestamp.
        Then after iterating through the pipe's contents.
        Then every record will contain a string key.
        And every record will contain a timestamp key.
        And the timestamp key will have an arrow value.
