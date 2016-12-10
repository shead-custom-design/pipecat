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

"""Pipecat is designed to work equally well with Python 2 and Python 3
using a single codebase.  This module provides definitions and functionality
to help pipecat contributors write portable code.  End-users should not need
any of the functionality in this module.
"""

from __future__ import absolute_import, division, print_function

try:
    string_type = basestring
except:  # pragma: no cover pylint: disable=bare-except
    string_type = str

try:
    basestring # pylint: disable=pointless-statement
    unicode_type = unicode
except:  # pragma: no cover pylint: disable=bare-except
    unicode_type = str

try:
    bytes_type = bytes
except:  # pragma: no cover pylint: disable=bare-except
    bytes_type = str
