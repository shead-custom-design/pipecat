# Copyright 2016 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functions for storing data.
"""

from __future__ import absolute_import, division, print_function

import os

import datacat

class Cache(object):
    """Cache records in memory for column-oriented access."""
    def __init__(self, source):
        self._source = source
        self._storage = datacat.Table()

    def __iter__(self):
        return self

    def next(self):
        record = self._source.next()
        self._storage.append(record)
        return record

    @property
    def table(self):
        return self._storage

def cache(source):
    """Create an in-memory cache for records.

    Parameters
    ----------
    source: generator, required
        A source of records to be cached.

    Return
    ------
    cache: instance of :class:`datacat.storage.Cache`.
    """
    return Cache(source)

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

