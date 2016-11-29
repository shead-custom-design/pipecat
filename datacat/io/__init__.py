"""Functions for performing I/O.
"""

from __future__ import absolute_import, division, print_function

import os

import datacat

def csv(source, fobj):
    """Append records to a CSV file."""
    def implementation(source, fobj): # pylint: disable=missing-docstring
        index = None
        fobj.seek(0, os.SEEK_SET)
        for line in fobj:
            index = line.split(",")[0]
        fobj.seek(0, os.SEEK_END)

        if index is not None:
            index = int(index) + 1
        else:
            index = 0

        for record in source:
            for key, value in sorted(record.items()):
                fobj.write("%s,%s,%s\n" % (index, key, value))
            index += 1
            yield record

    if isinstance(fobj, basestring):
        with open(fobj, "a+b") as fobj:
            for record in implementation(source, fobj):
                yield record
    else:
        for record in implementation(source, fobj):
            yield record

