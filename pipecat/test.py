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


def mock_module(module):
    sys.modules[module] = mock.Mock()
    return sys.modules[module]


def read_file(path, rate=None, start=None, stop=None, step=None, block=False):
    if rate is not None:
        rate = rate.to(pipecat.units.seconds).magnitude

    def implementation(*args, **kwargs):
        for line in itertools.islice(open(path, "r"), start, stop, step):
            yield line
            if rate is not None:
                time.sleep(rate)
        if block:
            while True:
                time.sleep(1)

    return implementation


class ReceiveFromFile(object):
    def __init__(self, path, client, rate, start, stop, step, block):
        if rate is not None:
            rate = rate.to(pipecat.units.seconds).magnitude

        self._stream = itertools.islice(open(path, "r"), start, stop, step)
        self._client = client
        self._rate = rate
        self._block = block

    def __call__(self, maxsize):
        try:
#            if rate is not None:
#                time.sleep(rate)
            return next(self._stream), self._client
        except StopIteration as e:
            if self._block:
                while True:
                    time.sleep(1)
            else:
                raise e


def recvfrom_file(path, client, rate=None, start=None, stop=None, step=None, block=False):
    return ReceiveFromFile(path=path, client=client, rate=rate, start=start, stop=stop, step=step, block=block)
