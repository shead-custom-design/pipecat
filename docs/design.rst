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
hardware devices produce records, filter functions consume input records and
produce modified output records, and storage functions serialize records to
other media.  A record could represent a location reported by the GPS in your
phone, an OBD-II reading from your car's diagnostic computer, or the state of a
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
as we go.  The intention is to encourage developers of new Pipecat components
to think broadly about the type of data they store in records.  The one
exception to this permissive approach is that Pipecat requires code to use
tuples-of-strings to represent hierarchies of keys.  Representing hierarchies
in this way makes them explicit and avoids imposed or inconsistent naming
schemes such as the use of slashes or (ack!) backslashes.

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
produces records.  Some examples of record generators include:

* :func:`pipecat.utility.readline`, which returns a record for each line in a file or file-like object.
* :func:`pipecat.udp.receive`, which returns a record for each message received on a listening UDP port.

.. _record-consumers:

Record Consumers
----------------

Record consumers are any function or object that consumes records, i.e.
iterates over the results of a record generator.  Some examples of record consumers include:

* :func:`pipecat.queue.send`, which places records consumed from a generator sequentially into a :class:`queue.Queue`.

.. _record-filters:

Record Filters
--------------

Record filters are any function or object that both consumes and generates records.  Examples include:

* :func:`pipecat.utility.add_timestamp`, which adds a timestamp field to the records it receives.
* :func:`pipecat.device.gps.nmea`, which takes records containing strings and converts them into records containing navigational information.

