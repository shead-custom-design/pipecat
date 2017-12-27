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

import io
import os

from behave import *
import arrow
import nose.tools
import six

import pipecat.store

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
reference_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reference"))


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


@when(u'iterating through the pipe contents.')
def step_impl(context):
    context.records = []
    for record in context.pipe:
        context.records.append(record)


@then(u'{count} records will be returned.')
def step_impl(context, count):
    nose.tools.assert_equal(len(context.records), int(count))


@then(u'every record will contain a {key} key with a string value.')
def step_impl(context, key):
    key = eval(key)
    for record in context.records:
        nose.tools.assert_in(key, record)
        nose.tools.assert_is_instance(record[key], six.string_types)


@then(u'every record will contain a {key} key with a bytes value.')
def step_impl(context, key):
    key = eval(key)
    for record in context.records:
        nose.tools.assert_in(key, record)
        nose.tools.assert_is_instance(record[key], six.binary_type)


@then(u'every record will contain a {key} key with an arrow value.')
def step_impl(context, key):
    key = eval(key)
    for record in context.records:
        nose.tools.assert_in(key, record)
        nose.tools.assert_is_instance(record[key], arrow.arrow.Arrow)


@then(u'every record will contain a {key} key with an address value.')
def step_impl(context, key):
    key = eval(key)
    for record in context.records:
        nose.tools.assert_in(key, record)
        nose.tools.assert_is_instance(record[key], tuple)
        nose.tools.assert_equal(len(record[key]), 2)
        nose.tools.assert_is_instance(record[key][0], six.string_types)
        nose.tools.assert_is_instance(record[key][1], int)


@given(u'a pyserial connection.')
def step_impl(context):
    import serial
    context.pipe = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)


@given(u'a string stream.')
def step_impl(context):
    context.stream = io.StringIO()


@then(u'the stream contents will match {filename}')
def step_impl(context, filename):
	with open(os.path.join(reference_dir, filename), "r") as reference:
		nose.tools.assert_equal(reference.read(), context.stream.getvalue())


