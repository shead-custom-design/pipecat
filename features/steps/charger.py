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
# Copyright 2016 Timothy M. Shead

import os

from behave import *
import nose.tools

import pipecat.device.charger
import pipecat.test

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

@given(u'an icharger 208b connected to a serial port.')
def step_impl(context):
    serial = pipecat.test.mock_module("serial")
    serial.serial_for_url.side_effect = pipecat.test.read_file(os.path.join(data_dir, "icharger208b-charging"), stop=10)


@given(u'an instance of pipecat.device.charger.icharger208b')
def step_impl(context):
    context.pipe = pipecat.device.charger.icharger208b(context.pipe)
