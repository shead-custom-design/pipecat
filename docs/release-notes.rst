.. image:: ../artwork/pipecat.png
  :width: 200px
  :align: right

.. _release-notes:

Release Notes
=============

Pipecat 0.3.0 - May 27th, 2017
------------------------------

* Added support for motion capture on iOS devices.
* pipecat.record.dump() immediately flushes its output.
* Add sample GPS data.
* Set the Pint application registry when reading records with pipecat.store.pickle.read()
* Added support for OBD-II devices.
* Add example limits to the battery charger section of the user guide.
* Clarify the different between client and listener addresses for pipecat.udp.receive()
* Stub-out the GPS receiver section of the user guide.
* Add a new module for filtering records.
* Update testing code and expand the section on GPS receivers in the user guide.
* Ensure that pipecat.limit shuts-down upstream sources when terminated.
* Shutdown upstream generators for real this time.
* Handle KeyboardInterrupt gracefully within pipecat.limit.
* Add support for individual cell voltages in pipecat.device.charger.icharger_208b().
* Add a sample executable that monitors battery charger status, `pipecat-charger-status`.
* Add pipecat.device.serial.readline() for reliably retrieving lines of text from a serial port.
* Make all threads daemon threads so callers can shutdown normally.
* charging-status handles the case where no data has been received.
* Make the poll rate configurable for pipecat.device.serial.readline().
* Include the charger mode in charging-status output.
* Add functionality to retrieve data using HTTP requests.
* Add functionality to parse XML data.
* Add functionality to parse METAR weather data.
* Create a sample weather-monitoring application, `pipecat-wind-status`.
* Added pipecat.filter.duplicates().
* Add an option to clear pipecat.store.Table so caches can be emptied.
* Improve the logic for extracting METAR data from XML.
* Add exception handling to pipecat.xml.parse() and pipecat.http.get().
* Added separate loggers for pipecat.http and pipecat.xml.

Pipecat 0.2.0 - December 28th, 2016
-----------------------------------

* Improved documentation.
* Added sample charger data.
* Consolidated redundant file-management code.

Pipecat 0.1.0 - December 14th, 2016
-----------------------------------

* Initial Release
