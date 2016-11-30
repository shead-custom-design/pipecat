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

from __future__ import absolute_import, division, print_function

import sys

import datacat

def dump(record, fobj=sys.stdout):
    """Dump a human-readable text representation of a record to a file-like object.

    Parameters
    ----------
    record: dict, required
        Dictionary of key-value pairs to be written-out.
    fobj: file-like object, optional
    """

    for key, value in sorted(record.items()):
        if isinstance(key, tuple):
            key = "/".join(key)
        fobj.write("%s: %s\n" % (key, value))
    fobj.write("\n")


def add_field(record, key, value):
    """Add a key-value pair to a record.

    Parameters
    ----------
    record: dict, required
        Dictionary of key-value pairs that constitute a record.
    key: string or tuple of strings, required
        Record key to be overwritten.
    value: object
        New record value.
    """

    if key in record:
        datacat.log.warning("Overwriting %s=%s with %s=%s", key, record[key], key, value)
    record[key] = value

