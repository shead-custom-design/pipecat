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

For interoperability, Pipecat requires (with one exception) that record keys be
strings.  Using strings as keys makes records easy to understand, manipulate,
and serialize, while allowing great flexibility in the choice of keys for
devices.  Pipecat intentionally does not impose any naming scheme on record
keys, although we plan to evolve consistent sets of well-defined keys for
specific device classes as we go.  Our desire is to encourage developers of new
Pipecat components to think broadly about the type of data they store in
records.  The one exception to the permissive "strings-as-keys" approach is
that Pipecat encourages developers to use "hierarchical" keys where
appropriate, and requires that hierarchical keys be represented using
tuples-of-strings.  For example, a battery charger with both internal and
external temperature sensors should use `("temperature", "internal")` as a key
instead of some other private naming scheme such as `"temperature-internal"`,
`"temperature/internal"`, `"temperature|internal"`, etc.  Representing
hierarchies in this way makes them explicit, avoids a proliferation of private
naming schemes for hierarchical data, and allows downstream components to
manipulate hierarchical keys in a consistent way.

.. _record-values:

Record Values
-------------

Any type can be used as a value in a Pipecat record, and the goal again is to
avoid needlessly constraining the ingenuity of Pipecat developers.  There
are just two caveats:

* We strongly encourage the use of `Arrow <http://arrow.readthedocs.io>`_ objects to store timestamp data.  Arrow is already a required dependency of Pipecat, so it's guaranteed to be available.
* We strongly encourage the use of explicit physical units wherever possible.  Pipecat provides builtin quantity and unit support from `Pint <http://pint.readthedocs.io>`_ to make this easy.  Again, Pint is a required Pipecat dependency, so it's guaranteed available for Pipecat developers.

.. _record-generators:

Record Generators
-----------------

Record generators are any iterable expression (function or object) that
produces records.  An iterable expression is any expression that can be used as
with the Python `for` statement, and you use `for` loops to read
records from generators::

    generator = pipecat.device.clock.metronome()
    for record in generator:
        pipecat.record.dump(record)

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
records.  Most of the components provided by Pipecat fall into this category.
Examples include:

* :func:`pipecat.utility.add_timestamp`, which adds a timestamp field to the records it receives.
* :func:`pipecat.device.charger.icharger208b`, which takes records containing strings and converts them into records containing battery charging information.
* :func:`pipecat.device.gps.nmea`, which takes records containing strings and converts them into records containing navigational information.
* :func:`pipecat.limit.duration`, which passes records without modification until a fixed time interval has expired.

Pipes
-----

When all is said and done, you use Pipecat by hooking-together components to
create `pipes` that retrieve, process, and store records as part of some larger
task.  In the following example, we retrieve data from a battery charger
connected via a serial port, and print it to the console:

.. code-block:: python

    pipe = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
    pipe = pipecat.utility.readline(pipe)
    pipe = pipecat.device.charger.icharger208b(pipe)
    for record in pipe:
        pipecat.record.dump(record)

If we want to save the records to a CSV file, we simply add an additional component
to the pipe:

.. code-block:: python
    :emphasize-lines: 4

    pipe = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
    pipe = pipecat.utility.readline(pipe)
    pipe = pipecat.device.charger.icharger208b(pipe)
    pipe = pipecat.store.csv.write(pipe, "battery.csv")
    for record in pipe:
        pipecat.record.dump(record)

Note from this example how we use a single variable to keep track of the
"output" end of the pipe, passing it as the "input" to each component that we
connect.  Of course, nothing requires that you re-use a variable in this way,
but we find that this style avoids a proliferation of otherwise unused symbols
and makes reordering, adding and subtracting components in a pipe much easier.
For example, it's easy to comment-out the component we just added without
affecting any downstream code:

.. code-block:: python
    :emphasize-lines: 4

    pipe = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
    pipe = pipecat.utility.readline(pipe)
    pipe = pipecat.device.charger.icharger208b(pipe)
    #pipe = pipecat.store.csv.write(pipe, "battery.csv")
    for record in pipe:
        pipecat.record.dump(record)

Similarly, you can easily insert and reorder components without having to worry
about renaming variables.  Here, we add a component to timestamp the battery
charger records, and another component to automatically stop iteration after
five seconds of inactivity:

.. code-block:: python
    :emphasize-lines: 4,5

    pipe = serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000)
    pipe = pipecat.utility.readline(pipe)
    pipe = pipecat.device.charger.icharger208b(pipe)
    pipe = pipecat.utility.add_timestamp(pipe)
    pipe = pipecat.limit.timeout(pipe, timeout=pipecat.quantity(5, pipecat.units.seconds))
    pipe = pipecat.store.csv.write(pipe, "battery.csv")
    for record in pipe:
        pipecat.record.dump(record)

