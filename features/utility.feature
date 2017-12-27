Feature: pipecat.utility

    Scenario: pipecat.utility.readline
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        When iterating through the pipe contents.
        Then 1390 records will be returned.
        And every record will contain a "line" key with a string value.

    Scenario: pipecat.utility.add_timestamp
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.utility.add_timestamp.
        When iterating through the pipe contents.
        Then every record will contain a "line" key with a string value.
        And every record will contain a "timestamp" key with an arrow value.
