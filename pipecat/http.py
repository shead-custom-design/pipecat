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

"""Functions for working with HTTP requests.
"""

from __future__ import absolute_import, division, print_function

from six.moves import BaseHTTPServer
import logging
import time

import requests

import pipecat.record

log = logging.getLogger(__name__)


def get(*args, **kwargs):
    """Retrieve data using HTTP requests.

    Accepts the same parameters as :func:`requests.get`, plus the following:

    Parameters
    ----------
    poll: time quantity, optional.
        Time to wait between requests.

    Yields
    ------
    record: dict
        Records will contain `status`, `(header, key)`, `encoding`, and `body`
        keys containing the results returned from each request.
    """
    poll = kwargs.pop("poll", pipecat.quantity(5, pipecat.units.seconds)).to(pipecat.units.seconds).magnitude

    while True:
        try:
            result = requests.get(*args, **kwargs)

            record = {}
            pipecat.record.add_field(record, "status", result.status_code)
            for key, value in result.headers.items():
                pipecat.record.add_field(record, ("header", key), value)
            pipecat.record.add_field(record, "encoding", result.encoding)
            pipecat.record.add_field(record, "body", result.text)

            yield record
        except Exception as e:
            log.error(e)

        time.sleep(poll)


def receive(
    address,
    include_body=True,
    include_client=False,
    include_method=False,
    include_path=False,
    include_version=False,
    ):
    """Receives data sent using HTTP requests.

    Provides a simple HTTP server that receives client requests, converting
    each request into Pipecat records.

    Parameters
    ----------
    address: (host, port) tuple, required
        TCP address and IP port to be bound for listening to requests.

    Yields
    ------
    record: dict
        Records will contain `client`, `version`, `method`, `path`, and `body` keys containing
        the content of each request.
    """
    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        server_version = "Pipecat/" + pipecat.__version__

        record = {}

        def create_record(self):
            request_size = int(self.headers.get("Content-length", 0))

            Handler.record.clear()
            if include_body:
                pipecat.record.add_field(Handler.record, "body", self.rfile.read(request_size))
            if include_client:
                pipecat.record.add_field(Handler.record, "client", self.client_address)
            if include_method:
                pipecat.record.add_field(Handler.record, "method", self.command)
            if include_path:
                pipecat.record.add_field(Handler.record, "path", self.path)
            if include_version:
                pipecat.record.add_field(Handler.record, "version", self.request_version)

            self.send_response(200)
            self.end_headers()

        def do_GET(self):
            self.create_record()

        def do_PUT(self):
            self.create_record()

        def do_POST(self):
            self.create_record()

        def do_DELETE(self):
            self.create_record()

        def log_message(self, format, *args):
            log.debug(format, *args)

    server = BaseHTTPServer.HTTPServer(address, Handler)

    while True:
        server.handle_request()
        yield Handler.record

