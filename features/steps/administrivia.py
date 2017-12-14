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

import os
import pkgutil
import subprocess
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
docs_dir = os.path.join(root_dir, "docs")
package_dir = os.path.join(root_dir, "pipecat")

copyright_notice = """# Copyright 2016 Timothy M. Shead
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
"""

portability_imports = """from __future__ import absolute_import, division, print_function
"""


@given(u'all sources.')
def step_impl(context):
    context.sources = []
    for directory, subdirectories, filenames in os.walk(root_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] not in [".py"]:
                continue

            context.sources.append(os.path.join(directory, filename))
    context.sources = sorted(context.sources)


@then(u'every source must contain a copyright notice.')
def step_impl(context):
    for source in context.sources:
        with open(source, "r") as fobj:
            if not fobj.read().startswith(copyright_notice):
                raise AssertionError("%s missing copyright notice." % source)


@given(u'all package sources.')
def step_impl(context):
    context.sources = []
    for directory, subdirectories, filenames in os.walk(package_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] not in [".py"]:
                continue

            context.sources.append(os.path.join(directory, filename))
    context.sources = sorted(context.sources)


@then(u'every source must contain portability imports.')
def step_impl(context):
    for source in context.sources:
        with open(source, "r") as fobj:
            if portability_imports not in fobj.read():
                raise AssertionError("%s missing portability imports." % source)


@given(u'pylint')
def step_impl(context):
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, "pylint")):
            context.pylint = os.path.join(path, "pylint")
            return
    context.scenario.skip(reason="The pylint command is not available.")


@then(u'all pylint tests must pass without any messages.')
def step_impl(context):
    command = [context.pylint, package_dir]
    pylint = subprocess.check_call(command)
