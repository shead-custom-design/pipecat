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

"""Functions for working with UDP messages.
"""

from __future__ import absolute_import, division, print_function

import socket

import pipecat.record

def receive(address, maxsize):
    """Receive messages from a UDP socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    while True:
        string, address = s.recvfrom(maxsize)

        record = {}
        pipecat.record.add_field(record, "string", string)
        pipecat.record.add_field(record, "address", address)

        yield record

