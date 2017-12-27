Feature: pipecat.udp

    Scenario:
        Given an instance of pipecat.udp.receive.
        And an instance of pipecat.limit.count set to 3
        When sending 3 messages to the udp port from a separate thread.
        And iterating through the pipe contents.
        Then every record will contain a "client" key with an address value.
        And every record will contain a "message" key with a bytes value.

