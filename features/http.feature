Feature: pipecat.http

    Scenario:
        Given an instance of pipecat.http.receive.
        And an instance of pipecat.limit.count set to 3
        When sending 3 messages to the http port from a separate thread.
        And iterating through the pipe contents.
        Then every record will contain a "body" key with a bytes value.
        And every record will contain a "client" key with an address value.
        And every record will contain a "method" key with a string value.
        And every record will contain a "path" key with a string value.
        And every record will contain a "version" key with a string value.

