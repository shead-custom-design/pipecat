.. _user-guide:

.. image:: ../artwork/pipecat.png
  :width: 200px
  :align: right

User Guide
==========

.. _records:

Records
-------

All components in Pipecat manipulate `records`, which are plain Python dicts -
hardware devices produce records, helper functions consume input records and
produce output records, and storage functions serialize records to other media.
A record could represent your current location reported by the GPS in your
phone, or an OBD-II reading from your car's diagnostic computer, or the state
of a battery that's in a charger.  Because a record is a dict, it can contain
as many key-value pairs as are needed for any device, and you can manipulate
that data easily.

.. _record-keys:

Record Keys
-----------

Pipecat requires that record keys are either strings, or tuples-of-strings.
Using strings makes records easy to understand, manipulate, and serialize,
while leaving great flexibility for implementations.  Pipecat does not
currently impose any naming scheme or well-defined keys for any particular
purpose, although we plan to evolve consistent sets of keys for specific
device classes as we go.  The one exception to this permissive approach is
that Pipecat requires code to use tuples-of-strings for hierarchical keys.
Representing hierarchies in this way makes them explicit and avoids
imposing naming schemes such as the use of slashes or (ack!) backslashes.

.. _record-values:

Record Values
-------------



.. _record-generators:

Record Generators
-----------------

.. _record-consumers:

Record Consumers
----------------

