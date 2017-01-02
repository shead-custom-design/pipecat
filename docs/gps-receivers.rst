
.. image:: ../artwork/pipecat.png
    :width: 200px
    :align: right

.. gps-receivers:

GPS Receivers
-------------

Most GPS receivers have data logging capabilities that you can use with
Pipecat to view navigational information. Some receivers connect to your
computer via a serial port or a serial-over-USB cable that acts like a
traditional serial port. Others can push data to a network socket. For
this demonstration, we will receive GPS data sent from an iPhone to a
UDP socket:

.. code:: python

    import pipecat.record
    import pipecat.udp
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    for record in pipe:
        pipecat.record.dump(record)


.. parsed-literal::

    client: 172.10.0.20
    string: $GPTXT,01,01,07,Pipecat*12
    
    
    client: 172.10.0.20
    string: $GPGGA,164100,3511.33136,N,10643.48435,W,1,8,0.9,1654.0,M,46.9,M,0,2*50
    
    
    client: 172.10.0.20
    string: $GPRMC,164100,A,3511.33136,N,10643.48435,W,0.00,0.00,311216,003.1,W*7C
    
    
    client: 172.10.0.20
    string: $GPGLL,3511.33136,N,10643.48435,W,164100,A*36
    
    
    client: 172.10.0.20
    string: $HCHDG,129.5,,,8.7,E*29
    
    
    client: 172.10.0.20
    string: $PASHR,164100190,138.24,T,+32.56,+48.49,+00.00,3.141,3.141,35.000,1,0*17
    
    


Here, we used :func:`pipcat.udp.receive` to open a UDP socket
listening on port 7777 on all available network interfaces ("0.0.0.0")
and convert the received messages into Pipecat :ref:`records`, which
we dump to the console. Note that each record includes the IP address of
the client (the phone in this case), along with a string containing the
raw data of the message. In this case the raw data is in NMEA format, a
widely-used standard for exchanging navigational data. To decode the
contents of each message, we add the appropriate Pipecat device to the
end of the pipe:

.. code:: python

    import pipecat.device.gps
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe)
    for record in pipe:
        pipecat.record.dump(record)


.. parsed-literal::

    id: GPTXT
    text: Pipecat
    
    altitude: 1654.0 meter
    dop: 0.9
    geoid-height: 46.9 meter
    id: GPGGA
    latitude: 35.188856 degree
    longitude: -106.724739167 degree
    quality: 1
    satellites: 8
    time: 164100
    
    active: True
    date: 311216
    id: GPRMC
    latitude: 35.188856 degree
    longitude: -106.724739167 degree
    speed: 0.0 knot
    time: 164100
    track: 0.0 degree
    variation: -3.1 degree
    
    active: True
    id: GPGLL
    latitude: 35.188856 degree
    longitude: -106.724739167 degree
    time: 164100
    
    heading: 129.5 degree
    id: HCHDG
    variation: 8.7 degree
    
    heading: 138.24 degree
    heading-accuracy: 35.0 degree
    heave: 0.0 meter
    id: PASHR
    pitch: 48.49 degree
    pitch-accuracy: 3.141 degree
    roll: 32.56 degree
    roll-accuracy: 3.141 degree
    time: 164100190
    


As you can see, :func:`pipecat.device.gps.nmea` has converted the raw
NMEA messages into records containing human-readable navigational fields
with appropriate physical units. Note that unlike the
:ref:`battery-chargers` example, not every record produced by the GPS
receiver has the same fields. The NMEA standard includes many different
*types* of messages, and most GPS receivers will produce more than one
type. This will increase the complexity of our code - for example, we
will have to test for the presence of a field before extracting it from
a record:

.. code:: python

    import pipecat.device.gps
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe)
    for record in pipe:
        if "latitude" in record:
            print("Latitude:", record["latitude"], "Longitude:", record["longitude"])


.. parsed-literal::

    Latitude: 35.1949926667 degree Longitude: -106.7111135 degree
    Latitude: 35.1949926667 degree Longitude: -106.7111135 degree
    Latitude: 35.1949926667 degree Longitude: -106.7111135 degree
    Latitude: 35.1952843333 degree Longitude: -106.710192667 degree
    Latitude: 35.1952843333 degree Longitude: -106.710192667 degree
    Latitude: 35.1952843333 degree Longitude: -106.710192667 degree


... alternatively, you might key your code off a specific type of
message, using the ``id`` field.

As always, you can convert units safely and explicitly:

.. code:: python

    import pipecat.device.gps
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe)
    for record in pipe:
        if "speed" in record:
            print(record["speed"].to(pipecat.units.mph))


.. parsed-literal::

    39.9320468464 mph
    40.0586325857 mph
    40.1276793526 mph
    38.5626193033 mph

