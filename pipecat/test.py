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

"""Functionality for testing / documentation."""

from __future__ import absolute_import, division, print_function

import itertools
import sys
import time

import mock

import pipecat

def mock_serial_port():
    sys.modules["serial"] = mock.Mock()
    return sys.modules["serial"]

def read_file(mocked, path, rate=pipecat.quantity(0, pipecat.units.seconds), start=None, stop=None, step=None):
    rate = rate.to(pipecat.units.seconds).magnitude
    def implementation(*args, **kwargs): # pylint: disable=unused-argument
        for line in itertools.islice(open(path, "r"), start, stop, step):
            yield line
            time.sleep(rate)
    mocked.side_effect = implementation

