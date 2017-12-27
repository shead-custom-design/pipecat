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

from behave import *
import nose.tools

import socket
import threading
import time

import pipecat.udp

import test

@given(u'an instance of pipecat.udp.receive listening to a udp port.')
def step_impl(context):
    context.address = test.get_free_address()
    context.pipe = pipecat.udp.receive(context.address, 1024)

@when(u'sending {count} messages to the udp port from a separate thread.')
def step_impl(context, count):
    def implementation(count, address):
        time.sleep(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for index in range(count):
            s.sendto("foo", address)

    thread = threading.Thread(target=implementation, args=(int(count), context.address))
    thread.start()

