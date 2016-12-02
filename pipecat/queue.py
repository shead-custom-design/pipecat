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

"""Communication with Queue.Queue."""

from __future__ import absolute_import, division, print_function

def receive(queue):
    """Receive records from a queue."""
    while True:
        record = queue.get()
        if record is StopIteration:
            break
        yield record

def send(source, queue):
    """Send records from a source to a queue."""
    for record in source:
        queue.put(record)
    queue.put(StopIteration)

