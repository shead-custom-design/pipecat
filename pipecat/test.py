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
import pickle
import sys
import time

import mock

import pipecat

def mock_obd():
    sys.modules["obd"] = mock.Mock()
    return sys.modules["obd"]

def mock_serial():
    sys.modules["serial"] = mock.Mock()
    return sys.modules["serial"]

def read_file(mocked, path, rate=None, start=None, stop=None, step=None, block=False):
    if rate is not None:
        rate = rate.to(pipecat.units.seconds).magnitude

    def implementation(*args, **kwargs): # pylint: disable=unused-argument
        for line in itertools.islice(open(path, "r"), start, stop, step):
            yield line
            if rate is not None:
                time.sleep(rate)
        if block:
            while True:
                time.sleep(1)

    mocked.side_effect = implementation

