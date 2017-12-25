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

"""Functions for working with UDP messages.
"""

from __future__ import absolute_import, division, print_function

import socket

import pipecat.record


def receive(address, maxsize):
    """Receive messages from a UDP socket.

    Parameters
    ----------
    address: (host, port) tuple, required
        TCP address and IP port to be bound for listening for UDP packets.
    maxsize: int, required
        Maximum length of packets returned from the UDP socket.

    Yields
    ------
    record: dict
        Records will contain a `client` field with the address of the sending
        client, and a `message` field containing the content of the message.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    while True:
        message, client = s.recvfrom(maxsize)

        record = {}
        pipecat.record.add_field(record, "client", client)
        pipecat.record.add_field(record, "message", message)

        yield record
