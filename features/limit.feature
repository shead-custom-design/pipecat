Feature: pipecat.limit

    Scenario: pipecat.limit.count
        Given a file named icharger208b-charging.
        And an instance of pipecat.utility.readline.
        And an instance of pipecat.limit.count set to 5
        And after iterating through the pipe contents.
        Then 5 records will be returned.
