Feature: Administrivia

    Scenario:
        Given all sources.
        Then every source must contain a copyright notice.

    Scenario:
        Given all package sources.
        Then every source must contain portability imports.

    Scenario:
        Given pylint
        Then all pylint tests must pass without any messages.
