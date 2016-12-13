.. _design:

.. image:: ../artwork/pipecat.png
  :width: 200px
  :align: right

Design
======

.. _records:

Records
-------

Components in Pipecat manipulate `records`, which are plain Python dicts -
record generators (such as hardware devices) produce records as output, record
filters consume records as input and produce modified records as output, while
record consumers (such as functions that store data) only take records as
input.  A record could represent a location reported by the GPS in your phone,
an OBD-II reading from your car's diagnostic computer, or the state of a
battery reported by a battery charger.  Because a record is a dict, it can
contain however many key-value pairs are appropriate for a given device, and
you can manipulate that data easily.

.. _record-keys:

Record Keys
-----------

For interoperability, Pipecat assumes that record keys are strings.  Using
string keys makes records easy to understand, manipulate, and serialize, while
allowing great flexibility in the choice of keys for implementations.  Pipecat
intentionally does not impose any naming scheme on record keys, although we
plan to evolve consistent sets of well-defined keys for specific device classes
as we go.  Our desire is to encourage developers of new Pipecat components to
think broadly about the type of data they store in records.  The one exception
to this permissive approach is that Pipecat requires the use of
tuples-of-strings to represent hierarchical keys.  For example, a battery
charger with multiple temperature sensors should use `("temperature", "internal")`
instead of `"temperature-internal"`, `"temperature/internal"`,
`"temperature|internal"`, or some other device-specific naming scheme.
Representing hierarchies in this way makes them explicit and avoids imposed or
inconsistent naming.

.. _record-values:

Record Values
-------------

Any type can be used as a value in a Pipecat record, and the goal again is to avoid
needlessly constraining the creation of new Pipecat components.  There are just two caveats:

* We strongly encourage the use of `arrow <http://arrow.readthedocs.io>`_ objects to store timestamp data.
* We strongly encourage the use of explicit physical units wherever possible.  Pipecat provides builtin quantity and unit support from `pint <http://pint.readthedocs.io>`_ to make this easy.

.. _record-generators:

Record Generators
-----------------

Record generators are any iterable expression (function or object) that
produces records.  An iterable expression is any expression that can be used as
the target of the Python `for` statement, and you use `for` loops to read
records from generators::

    >>> generator = pipecat.device.clock.metronome()
    >>> for record in generator:
    ...   pipecat.record.dump(record)

Some examples of record generators include:

* :func:`pipecat.device.clock.metronome`, which returns an empty record at fixed time intervals.
* :func:`pipecat.utility.readline`, which returns a record for each line in a file or file-like object.
* :func:`pipecat.udp.receive`, which returns a record for each message received on a listening UDP port.

.. _record-consumers:

Record Consumers
----------------

Record consumers are any function or object that consumes records, i.e.
iterates over the results of a record generator, returning nothing.  Some
examples of record consumers include:

* :func:`pipecat.queue.send`, which places records consumed from a generator sequentially into a :class:`queue.Queue`.

.. _record-filters:

Record Filters
--------------

Record filters are any function or object that both consumes and generates
records.  A majority of components provided by Pipecat fall into this category::

    >>> generator = pipecat.device.clock.metronome()
    >>> filter = pipecat.utility.add_timestamp(generator)
    >>> filter = pipecat.limit.duration(filter, duration=pipecat.quantity(5, pipecat.units.minutes))
    >>> for record in filter:
    ...   pipecat.record.dump(record)

Record filter examples include:

* :func:`pipecat.utility.add_timestamp`, which adds a timestamp field to the records it receives.
* :func:`pipecat.device.gps.nmea`, which takes records containing strings and converts them into records containing navigational information.

