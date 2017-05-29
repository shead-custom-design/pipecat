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
import arrow
import nose.tools

import pipecat.compatibility
import pipecat.store

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
print(data_dir)

@given(u'a file named {filename}.')
def step_impl(context, filename):
    context.pipe = open(os.path.join(data_dir, filename), "rb")

@given(u'an instance of pipecat.store.cache.')
def step_impl(context):
    context.pipe = pipecat.store.cache(context.pipe)

@then(u'the pipe can be iterated to completion.')
def step_impl(context):
    for record in context.pipe:
        pass

@then(u'after iterating through the pipe\'s contents.')
def step_impl(context):
    context.records = []
    for record in context.pipe:
        context.records.append(record)

@then(u'{count} records will be returned.')
def step_impl(context, count):
    nose.tools.assert_equal(len(context.records), int(count))

@then(u'every record will contain a {key} key.')
def step_impl(context, key):
    for record in context.records:
        nose.tools.assert_in(key, record)

@then(u'the {key} key will have a string value.')
def step_impl(context, key):
	for record in context.records:
		nose.tools.assert_is_instance(record[key], pipecat.compatibility.string_type)

@then(u'the {key} key will have an arrow value.')
def step_impl(context, key):
    for record in context.records:
		nose.tools.assert_is_instance(record[key], arrow.arrow.Arrow)

