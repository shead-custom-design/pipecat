# Copyright 2016 Timothy M. Shead
#
# This file is part of Pipecat.
#
# Pipecat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pipecat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pipecat.  If not, see <http://www.gnu.org/licenses/>.

"""Functions for reading and writing CSV data.
"""

from __future__ import absolute_import, division, print_function

import pipecat.store

def write(source, fobj):
    """Append records to a CSV file."""
    with pipecat.store._FileHelper(fobj, "a+b") as fobj:
        for record in source:
            start_record = 1
            for key, value in sorted(record.items()):
                fobj.write("%s,%s,%s\n" % (start_record, key, value))
                start_record = 0
            yield record

