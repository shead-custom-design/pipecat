
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
    message: $GPTXT,01,01,07,Pipecat*12
    
    
    client: 172.10.0.20
    message: $GPGGA,164100,3511.33136,N,10643.48435,W,1,8,0.9,1654.0,M,46.9,M,0,2*50
    
    
    client: 172.10.0.20
    message: $GPRMC,164100,A,3511.33136,N,10643.48435,W,0.00,0.00,311216,003.1,W*7C
    
    
    client: 172.10.0.20
    message: $GPGLL,3511.33136,N,10643.48435,W,164100,A*36
    
    
    client: 172.10.0.20
    message: $HCHDG,129.5,,,8.7,E*29
    
    
    client: 172.10.0.20
    message: $PASHR,164100190,138.24,T,+32.56,+48.49,+00.00,3.141,3.141,35.000,1,0*17
    
    


Here, we used :func:`pipecat.udp.receive` to open a UDP socket
listening on port 7777 on all available network interfaces ("0.0.0.0")
and convert the received messages into Pipecat :ref:`records`, which
we dump to the console. Note that each record includes the address of
the client (the phone in this case), along with a "message" field
containing the raw data of the message. In this case the raw data is in
NMEA format, a widely-used standard for exchanging navigational data. To
decode the contents of each message, we add the appropriate Pipecat
device to the end of the pipe:

.. code:: python

    import pipecat.device.gps
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
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
might have to test for the presence of a field before extracting it from
a record:

.. code:: python

    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
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


Alternatively, we might use the record ``id`` field to key our code off
a specific type of NMEA message:

.. code:: python

    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
    for record in pipe:
        if record["id"] == "PASHR":
            print("Pitch:", record["pitch"])


.. parsed-literal::

    Pitch: 66.82 degree
    Pitch: 67.3 degree
    Pitch: 66.8 degree
    Pitch: 66.18 degree


Another alternative would be to add a filter to our pipe so we only
receive records that match some criteria:

.. code:: python

    import pipecat.filter
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
    pipe = pipecat.filter.keep(pipe, key="id", value="GPGLL")
    for record in pipe:
        pipecat.record.dump(record)


.. parsed-literal::

    active: True
    id: GPGLL
    latitude: 35.1949926667 degree
    longitude: -106.7111135 degree
    time: 164252
    
    active: True
    id: GPGLL
    latitude: 35.1952843333 degree
    longitude: -106.710192667 degree
    time: 164257
    
    active: True
    id: GPGLL
    latitude: 35.1956116667 degree
    longitude: -106.709064 degree
    time: 164303
    
    active: True
    id: GPGLL
    latitude: 35.1958851667 degree
    longitude: -106.708156167 degree
    time: 164308
    


Note that :func:`pipecat.filter.keep` discards all records that don't
meet the given criteria, which allows our downstream code to rely on the
availability of specific fields.

Regardless of the logic you employ to identify fields of interest,
Pipecat always makes it easy to convert units safely and explicitly:

.. code:: python

    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
    for record in pipe:
        if "speed" in record:
            print(record["speed"].to(pipecat.units.mph))


.. parsed-literal::

    39.9320468464 mph
    40.0586325857 mph
    40.1276793526 mph
    38.5626193033 mph


Let's explore other things we can do with our pipe. To begin, you might
want to add additional metadata to the records returned from a device.
For example, if you were collecting data from multiple devices you might
want to "tag" records with a user-specific unique identifier:

.. code:: python

    import pipecat.utility
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
    pipe = pipecat.filter.keep(pipe, key="id", value="GPGLL")
    pipe = pipecat.utility.add_field(pipe, "serial", "1237V")
    for record in pipe:
        pipecat.record.dump(record)


.. parsed-literal::

    active: True
    id: GPGLL
    latitude: 35.1949926667 degree
    longitude: -106.7111135 degree
    serial: 1237V
    time: 164252
    
    active: True
    id: GPGLL
    latitude: 35.1952843333 degree
    longitude: -106.710192667 degree
    serial: 1237V
    time: 164257
    
    active: True
    id: GPGLL
    latitude: 35.1956116667 degree
    longitude: -106.709064 degree
    serial: 1237V
    time: 164303
    


Now let's consider calculating some simple statistics, such as our
average speed on a trip. When we iterate over the contents of a pipe
using a ``for`` loop, we receive one record at-a-time until the pipe is
empty. We could keep track of a "running" average during iteration, and
there are use-cases where that is the best way to solve the problem.
However, for moderately-sized data, Pipecat provides a more convenient
approach:

.. code:: python

    import pipecat.store
    pipe = pipecat.udp.receive(address=("0.0.0.0", 7777), maxsize=1024)
    pipe = pipecat.device.gps.nmea(pipe, key="message")
    pipe = pipecat.store.cache(pipe)
    for record in pipe:
        pass
    print(pipe.table["speed"])


.. parsed-literal::

    [  0.     0.    10.59  17.96   4.39  24.14  30.65  33.59  33.28  32.85  34.08  34.78  35.28  34.66  34.46  34.1   34.64  34.41  33.88  33.75  34.7   34.81  34.87  33.51  33.71  35.38  32.09  28.94  18.     0.     1.19  21.23  31.92  33.55  34.91  34.78  33.75  32.71  31.67  31.14  31.45  31.94  31.16  32.27  35.46  35.34  34.06  33.82  34.91  34.72  34.83  34.95  33.38  33.08  27.39   5.21   0.     2.45  22.68  33.1   33.8  34.64  33.96  34.37  34.81  32.75  29.55  21.71  13.8   14.48  27.29  25.21  11.68  13.86   9.16   0.  ] knot


Here, :func:`pipecat.store.cache` creates an in-memory cache that
stores every record it receives. We have a do-nothing ``for`` loop that
reads data from the charger to populate the cache. Once that's complete,
we can use the cache ``table`` attribute to retrieve data from the cache
using the same keys and syntax we would use with a record. Unlike a
record, the cache returns every value for a given key at once (using a
Numpy array), which makes it easy to compute the statistics we're
interested in:

.. code:: python

    print("Average speed:", pipe.table["speed"].mean().to(pipecat.units.mph))


.. parsed-literal::

    Average speed: 30.8533055116 mph


Consolidating fields using the cache is also perfect for generating
plots with a library like Toyplot (http://toyplot.readthedocs.io):

.. code:: python

    import toyplot
    
    canvas = toyplot.Canvas(width=600, height=400)
    axes = canvas.cartesian(grid=(2, 1, 0), xlabel="Record #", ylabel="Speed (MPH)")
    axes.plot(pipe.table["speed"].to(pipecat.units.mph))
    axes = canvas.cartesian(grid=(2, 1, 1), xlabel="Record #", ylabel="Track")
    axes.plot(pipe.table["track"]);



.. raw:: html

    <div class="toyplot" id="t88bd2e96c9c944be885aba13de048972" style="text-align:center"><svg class="toyplot-canvas-Canvas" height="400.0px" id="ted7ec029b3f747cf97ba6e72dae83f88" preserveAspectRatio="xMidYMid meet" style="background-color:transparent;fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:Helvetica;font-size:12px;opacity:1.0;stroke:rgb(16.1%,15.3%,14.1%);stroke-opacity:1.0;stroke-width:1.0" viewBox="0 0 600.0 400.0" width="600.0px" xmlns="http://www.w3.org/2000/svg" xmlns:toyplot="http://www.sandia.gov/toyplot" xmlns:xlink="http://www.w3.org/1999/xlink"><g class="toyplot-coordinates-Cartesian" id="t6ed6c7a8771f493586ffef3f87233743"><clipPath id="t9267f2a0c74742a6835e7b1fab0cffb4"><rect height="120.0" width="520.0" x="40.0" y="40.0"></rect></clipPath><g clip-path="url(#t9267f2a0c74742a6835e7b1fab0cffb4)"><g class="toyplot-mark-Plot" id="tb153daf1af954ab7a921aeaad1d5a657" style="fill:none"><g class="toyplot-Series"><path d="M 50.0 150.0 L 56.666666666666671 150.0 L 63.333333333333343 120.13536379018612 L 70.0 99.351381838691481 L 76.666666666666671 137.61985335589398 L 83.333333333333329 81.923293852227857 L 90.0 63.564579808234647 L 96.666666666666657 55.273547659334461 L 103.33333333333334 56.147772137619853 L 110.0 57.360406091370557 L 116.66666666666666 53.891708967851102 L 123.33333333333334 51.917653694303446 L 130.0 50.507614213197982 L 136.66666666666669 52.256063169768758 L 143.33333333333334 52.820078962210935 L 150.0 53.835307388606878 L 156.66666666666669 52.312464749012975 L 163.33333333333331 52.961082910321501 L 170.0 54.455724760293279 L 176.66666666666669 54.822335025380717 L 183.33333333333331 52.143260011280297 L 190.00000000000003 51.833051325437125 L 196.66666666666669 51.663846587704455 L 203.33333333333331 55.499153976311348 L 210.0 54.935138183869149 L 216.66666666666666 50.225606316976879 L 223.33333333333334 59.503666102650875 L 230.0 68.38691483361535 L 236.66666666666669 99.238578680203062 L 243.33333333333331 150.0 L 250.0 146.64410603496898 L 256.66666666666669 90.129723632261715 L 263.33333333333337 59.983079526226739 L 270.0 55.386350817822908 L 276.66666666666663 51.55104342921603 L 283.33333333333337 51.917653694303446 L 290.0 54.822335025380717 L 296.66666666666663 57.755217146080085 L 303.33333333333337 60.688099266779474 L 310.0 62.182741116751274 L 316.66666666666663 61.308516638465868 L 323.33333333333331 59.926677946982522 L 330.00000000000006 62.12633953750705 L 336.66666666666669 58.996051889452893 L 343.33333333333337 50.0 L 350.0 50.338409475465298 L 356.66666666666663 53.948110547095311 L 363.33333333333337 54.624929498025942 L 370.0 51.55104342921603 L 376.66666666666663 52.086858432036109 L 383.33333333333331 51.776649746192902 L 390.0 51.438240270727569 L 396.66666666666669 55.86576424139875 L 403.33333333333337 56.711787930062044 L 410.0 72.758037225042301 L 416.66666666666663 135.30738860688101 L 423.33333333333337 150.0 L 430.0 143.09080654258318 L 436.66666666666663 86.040609137055853 L 443.33333333333331 56.655386350817814 L 450.0 54.68133107727018 L 456.66666666666669 52.312464749012975 L 463.33333333333337 54.230118443316407 L 470.0 53.073886068809948 L 476.66666666666669 51.833051325437125 L 483.33333333333337 57.642413987591659 L 490.0 66.666666666666671 L 496.66666666666663 88.776085730400467 L 503.33333333333331 111.082910321489 L 510.0 109.16525662718557 L 516.66666666666674 73.040045121263404 L 523.33333333333326 78.905809362662154 L 530.0 117.06147772137621 L 536.66666666666674 110.91370558375635 L 543.33333333333326 124.16807670614779 L 550.0 150.0" style="stroke:rgb(40%,76.1%,64.7%);stroke-opacity:1.0;stroke-width:2.0"></path></g></g></g><g class="toyplot-coordinates-Axis" id="t618c0d13fcc141abb5628de92425c079" transform="translate(50.0,150.0)translate(0,10.0)"><line style="" x1="0" x2="500.0" y1="0" y2="0"></line><g><g transform="translate(0.0,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-2.78" y="8.555">0</text></g><g transform="translate(166.66666666666666,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">25</text></g><g transform="translate(333.3333333333333,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">50</text></g><g transform="translate(500.0,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">75</text></g></g><g transform="translate(250.0,22)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:12.0px;font-weight:bold;stroke:none;vertical-align:baseline;white-space:pre" x="-25.674" y="10.266">Record #</text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="-3.0" y2="4.5"></line><text style="alignment-baseline:alphabetic;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="-6"></text></g></g><g class="toyplot-coordinates-Axis" id="tf481b22bcfad4cf08c8ea85892222849" transform="translate(50.0,150.0)rotate(-90.0)translate(0,-10.0)"><line style="" x1="0" x2="100.0" y1="0" y2="0"></line><g><g transform="translate(0.0,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-2.78" y="-4.4408920985e-16">0</text></g><g transform="translate(24.505816184451437,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="-4.4408920985e-16">10</text></g><g transform="translate(49.01163236890287,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="-4.4408920985e-16">20</text></g><g transform="translate(73.51744855335431,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="-4.4408920985e-16">30</text></g><g transform="translate(98.02326473780575,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="-4.4408920985e-16">40</text></g></g><g transform="translate(50.0,-22)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:12.0px;font-weight:bold;stroke:none;vertical-align:baseline;white-space:pre" x="-37.002" y="0.0">Speed (MPH)</text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="3.0" y2="-4.5"></line><text style="alignment-baseline:hanging;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="6"></text></g></g></g><g class="toyplot-coordinates-Cartesian" id="ta11216f251934e9983177ca81f7adca7"><clipPath id="t535477d2d6404db9b3535cb6854f38ac"><rect height="120.0" width="520.0" x="40.0" y="240.0"></rect></clipPath><g clip-path="url(#t535477d2d6404db9b3535cb6854f38ac)"><g class="toyplot-mark-Plot" id="t57ef92861432432e81af535b8a8612f2" style="fill:none"><g class="toyplot-Series"><path d="M 50.0 350.0 L 56.666666666666671 349.25149700598803 L 63.333333333333343 342.2155688622754 L 70.0 348.20359281437123 L 76.666666666666671 343.8922155688623 L 83.333333333333329 323.41317365269458 L 90.0 323.17365269461072 L 96.666666666666657 323.23353293413174 L 103.33333333333334 323.05389221556885 L 110.0 322.63473053892216 L 116.66666666666666 324.1317365269461 L 123.33333333333334 327.69461077844306 L 130.0 330.56886227544913 L 136.66666666666669 329.82035928143716 L 143.33333333333334 329.79041916167665 L 150.0 329.10179640718565 L 156.66666666666669 329.10179640718565 L 163.33333333333331 329.10179640718565 L 170.0 329.25149700598803 L 176.66666666666669 329.19161676646706 L 183.33333333333331 328.44311377245509 L 190.00000000000003 328.95209580838326 L 196.66666666666669 329.16167664670661 L 203.33333333333331 329.16167664670661 L 210.0 329.04191616766462 L 216.66666666666666 327.90419161676652 L 223.33333333333334 326.19760479041918 L 230.0 324.64071856287421 L 236.66666666666669 323.59281437125748 L 243.33333333333331 323.47305389221555 L 250.0 323.47305389221555 L 256.66666666666669 296.85628742514973 L 263.33333333333337 296.22754491017963 L 270.0 292.21556886227546 L 276.66666666666663 284.01197604790417 L 283.33333333333337 283.59281437125748 L 290.0 283.80239520958082 L 296.66666666666663 283.59281437125748 L 303.33333333333337 283.80239520958082 L 310.0 283.68263473053889 L 316.66666666666663 284.43113772455092 L 323.33333333333331 285.14970059880238 L 330.00000000000006 285.56886227544908 L 336.66666666666669 284.43113772455092 L 343.33333333333337 281.67664670658684 L 350.0 278.20359281437129 L 356.66666666666663 272.09580838323353 L 363.33333333333337 270.32934131736528 L 370.0 270.02994011976045 L 376.66666666666663 273.86227544910179 L 383.33333333333331 278.20359281437129 L 390.0 280.92814371257487 L 396.66666666666669 281.01796407185628 L 403.33333333333337 281.01796407185628 L 410.0 281.13772455089821 L 416.66666666666663 281.13772455089821 L 423.33333333333337 281.13772455089821 L 430.0 281.13772455089821 L 436.66666666666663 254.07185628742516 L 443.33333333333331 254.22155688622755 L 450.0 254.07185628742516 L 456.66666666666669 254.07185628742516 L 463.33333333333337 254.07185628742516 L 470.0 254.07185628742516 L 476.66666666666669 255.38922155688621 L 483.33333333333337 261.88622754491018 L 490.0 264.73053892215569 L 496.66666666666663 268.23353293413174 L 503.33333333333331 269.10179640718565 L 510.0 250.0 L 516.66666666666674 349.91017964071858 L 523.33333333333326 349.97005988023955 L 530.0 337.27544910179643 L 536.66666666666674 329.79041916167665 L 543.33333333333326 334.31137724550899 L 550.0 334.94011976047904" style="stroke:rgb(40%,76.1%,64.7%);stroke-opacity:1.0;stroke-width:2.0"></path></g></g></g><g class="toyplot-coordinates-Axis" id="t424928479c104d3e9bcde462e3e9bb9a" transform="translate(50.0,350.0)translate(0,10.0)"><line style="" x1="0" x2="500.0" y1="0" y2="0"></line><g><g transform="translate(0.0,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-2.78" y="8.555">0</text></g><g transform="translate(166.66666666666666,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">25</text></g><g transform="translate(333.3333333333333,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">50</text></g><g transform="translate(500.0,6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-5.56" y="8.555">75</text></g></g><g transform="translate(250.0,22)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:12.0px;font-weight:bold;stroke:none;vertical-align:baseline;white-space:pre" x="-25.674" y="10.266">Record #</text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="-3.0" y2="4.5"></line><text style="alignment-baseline:alphabetic;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="-6"></text></g></g><g class="toyplot-coordinates-Axis" id="tbae6e97f30cb453d987319e0d71c9465" transform="translate(50.0,350.0)rotate(-90.0)translate(0,-10.0)"><line style="" x1="0" x2="100.0" y1="0" y2="0"></line><g><g transform="translate(0.0,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-2.78" y="-4.4408920985e-16">0</text></g><g transform="translate(29.94011976047904,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-8.34" y="-4.4408920985e-16">100</text></g><g transform="translate(59.88023952095808,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-8.34" y="-4.4408920985e-16">200</text></g><g transform="translate(89.82035928143712,-6)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:10.0px;font-weight:normal;stroke:none;vertical-align:baseline;white-space:pre" x="-8.34" y="-4.4408920985e-16">300</text></g></g><g transform="translate(50.0,-22)"><text style="fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:helvetica;font-size:12.0px;font-weight:bold;stroke:none;vertical-align:baseline;white-space:pre" x="-16.008" y="0.0">Track</text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="3.0" y2="-4.5"></line><text style="alignment-baseline:hanging;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="6"></text></g></g></g></svg><div class="toyplot-behavior"><script>(function()
    {
    var modules={};
    modules["toyplot/tables"] = (function()
        {
            var tables = [];
    
            var module = {};
    
            module.set = function(owner, key, names, columns)
            {
                tables.push({owner: owner, key: key, names: names, columns: columns});
            }
    
            module.get = function(owner, key)
            {
                for(var i = 0; i != tables.length; ++i)
                {
                    var table = tables[i];
                    if(table.owner != owner)
                        continue;
                    if(table.key != key)
                        continue;
                    return {names: table.names, columns: table.columns};
                }
            }
    
            module.get_csv = function(owner, key)
            {
                var table = module.get(owner, key);
                if(table != undefined)
                {
                    var csv = "";
                    csv += table.names.join(",") + "\n";
                    for(var i = 0; i != table.columns[0].length; ++i)
                    {
                      for(var j = 0; j != table.columns.length; ++j)
                      {
                        if(j)
                          csv += ",";
                        csv += table.columns[j][i];
                      }
                      csv += "\n";
                    }
                    return csv;
                }
            }
    
            return module;
        })();
    modules["toyplot/root/id"] = "t88bd2e96c9c944be885aba13de048972";
    modules["toyplot/root"] = (function(root_id)
        {
            return document.querySelector("#" + root_id);
        })(modules["toyplot/root/id"]);
    modules["toyplot/canvas/id"] = "ted7ec029b3f747cf97ba6e72dae83f88";
    modules["toyplot/canvas"] = (function(canvas_id)
        {
            return document.querySelector("#" + canvas_id);
        })(modules["toyplot/canvas/id"]);
    modules["toyplot/menus/context"] = (function(root, canvas)
        {
            var wrapper = document.createElement("div");
            wrapper.innerHTML = "<ul class='toyplot-context-menu' style='background:#eee; border:1px solid #b8b8b8; border-radius:5px; box-shadow: 0px 0px 8px rgba(0%,0%,0%,0.25); margin:0; padding:3px 0; position:fixed; visibility:hidden;'></ul>"
            var menu = wrapper.firstChild;
    
            root.appendChild(menu);
    
            var items = [];
    
            var ignore_mouseup = null;
            function open_menu(e)
            {
                var show_menu = false;
                for(var index=0; index != items.length; ++index)
                {
                    var item = items[index];
                    if(item.show(e))
                    {
                        item.item.style.display = "block";
                        show_menu = true;
                    }
                    else
                    {
                        item.item.style.display = "none";
                    }
                }
    
                if(show_menu)
                {
                    ignore_mouseup = true;
                    menu.style.left = (e.clientX + 1) + "px";
                    menu.style.top = (e.clientY - 5) + "px";
                    menu.style.visibility = "visible";
                    e.stopPropagation();
                    e.preventDefault();
                }
            }
    
            function close_menu()
            {
                menu.style.visibility = "hidden";
            }
    
            function contextmenu(e)
            {
                open_menu(e);
            }
    
            function mousemove(e)
            {
                ignore_mouseup = false;
            }
    
            function mouseup(e)
            {
                if(ignore_mouseup)
                {
                    ignore_mouseup = false;
                    return;
                }
                close_menu();
            }
    
            function keydown(e)
            {
                if(e.key == "Escape" || e.key == "Esc" || e.keyCode == 27)
                {
                    close_menu();
                }
            }
    
            canvas.addEventListener("contextmenu", contextmenu);
            canvas.addEventListener("mousemove", mousemove);
            document.addEventListener("mouseup", mouseup);
            document.addEventListener("keydown", keydown);
    
            var module = {};
            module.add_item = function(label, show, activate)
            {
                var wrapper = document.createElement("div");
                wrapper.innerHTML = "<li class='toyplot-context-menu-item' style='background:#eee; color:#333; padding:2px 20px; list-style:none; margin:0; text-align:left;'>" + label + "</li>"
                var item = wrapper.firstChild;
    
                items.push({item: item, show: show});
    
                function mouseover()
                {
                    this.style.background = "steelblue";
                    this.style.color = "white";
                }
    
                function mouseout()
                {
                    this.style.background = "#eee";
                    this.style.color = "#333";
                }
    
                function choose_item(e)
                {
                    close_menu();
                    activate();
    
                    e.stopPropagation();
                    e.preventDefault();
                }
    
                item.addEventListener("mouseover", mouseover);
                item.addEventListener("mouseout", mouseout);
                item.addEventListener("mouseup", choose_item);
                item.addEventListener("contextmenu", choose_item);
    
                menu.appendChild(item);
            };
            return module;
        })(modules["toyplot/root"],modules["toyplot/canvas"]);
    modules["toyplot/io"] = (function()
        {
            var module = {};
            module.save_file = function(mime_type, charset, data, filename)
            {
                var uri = "data:" + mime_type + ";charset=" + charset + "," + data;
                uri = encodeURI(uri);
    
                var link = document.createElement("a");
                if(typeof link.download != "undefined")
                {
                  link.href = uri;
                  link.style = "visibility:hidden";
                  link.download = filename;
    
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }
                else
                {
                  window.open(uri);
                }
            };
            return module;
        })();
    modules["toyplot.coordinates.Axis"] = (
            function(canvas)
            {
                function sign(x)
                {
                    return x < 0 ? -1 : x > 0 ? 1 : 0;
                }
    
                function mix(a, b, amount)
                {
                    return ((1.0 - amount) * a) + (amount * b);
                }
    
                function log(x, base)
                {
                    return Math.log(Math.abs(x)) / Math.log(base);
                }
    
                function in_range(a, x, b)
                {
                    var left = Math.min(a, b);
                    var right = Math.max(a, b);
                    return left <= x && x <= right;
                }
    
                function inside(range, projection)
                {
                    for(var i = 0; i != projection.length; ++i)
                    {
                        var segment = projection[i];
                        if(in_range(segment.range.min, range, segment.range.max))
                            return true;
                    }
                    return false;
                }
    
                function to_domain(range, projection)
                {
                    for(var i = 0; i != projection.length; ++i)
                    {
                        var segment = projection[i];
                        if(in_range(segment.range.bounds.min, range, segment.range.bounds.max))
                        {
                            if(segment.scale == "linear")
                            {
                                var amount = (range - segment.range.min) / (segment.range.max - segment.range.min);
                                return mix(segment.domain.min, segment.domain.max, amount)
                            }
                            else if(segment.scale[0] == "log")
                            {
                                var amount = (range - segment.range.min) / (segment.range.max - segment.range.min);
                                var base = segment.scale[1];
                                return sign(segment.domain.min) * Math.pow(base, mix(log(segment.domain.min, base), log(segment.domain.max, base), amount));
                            }
                        }
                    }
                }
    
                var axes = {};
    
                function display_coordinates(e)
                {
                    var current = canvas.createSVGPoint();
                    current.x = e.clientX;
                    current.y = e.clientY;
    
                    for(var axis_id in axes)
                    {
                        var axis = document.querySelector("#" + axis_id);
                        var coordinates = axis.querySelector(".toyplot-coordinates-Axis-coordinates");
                        if(coordinates)
                        {
                            var projection = axes[axis_id];
                            var local = current.matrixTransform(axis.getScreenCTM().inverse());
                            if(inside(local.x, projection))
                            {
                                var domain = to_domain(local.x, projection);
                                coordinates.style.visibility = "visible";
                                coordinates.setAttribute("transform", "translate(" + local.x + ")");
                                var text = coordinates.querySelector("text");
                                text.textContent = domain.toFixed(2);
                            }
                            else
                            {
                                coordinates.style.visibility= "hidden";
                            }
                        }
                    }
                }
    
                canvas.addEventListener("click", display_coordinates);
    
                var module = {};
                module.show_coordinates = function(axis_id, projection)
                {
                    axes[axis_id] = projection;
                }
    
                return module;
            })(modules["toyplot/canvas"]);
    (function(tables, context_menu, io, owner_id, key, label, names, columns, filename)
            {
                tables.set(owner_id, key, names, columns);
    
                var owner = document.querySelector("#" + owner_id);
                function show_item(e)
                {
                    return owner.contains(e.target);
                }
    
                function choose_item()
                {
                    io.save_file("text/csv", "utf-8", tables.get_csv(owner_id, key), filename + ".csv");
                }
    
                context_menu.add_item("Save " + label + " as CSV", show_item, choose_item);
            })(modules["toyplot/tables"],modules["toyplot/menus/context"],modules["toyplot/io"],"tb153daf1af954ab7a921aeaad1d5a657","data","plot data",["x", "y0"],[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75], [0.0, 0.0, 12.186754354569315, 20.667998886502826, 5.0519217768233515, 27.779815875288318, 35.271390081921574, 38.65468165911079, 38.297940030223494, 37.803104867573374, 39.218563588642326, 40.024109202258806, 40.59949892627058, 39.88601566849598, 39.655859778891276, 39.2415791776028, 39.86300007953551, 39.598320806490094, 38.98840769903762, 38.83880637079456, 39.93204684641693, 40.05863258569951, 40.12767935258093, 38.5626193032689, 38.79277519287362, 40.714576871072936, 36.92851248707548, 33.30355722580132, 20.714030064423763, 0.0, 1.3694275431480154, 24.43104768153981, 36.73287998091148, 38.60865048118985, 40.173710530501864, 40.024109202258806, 38.83880637079456, 37.64199574485008, 36.44518511890559, 35.835272011453114, 36.19201364034041, 36.755895569871946, 35.85828760041358, 37.13565278771972, 40.80663922691482, 40.668545693152, 39.19554799968186, 38.91936093215621, 40.173710530501864, 39.95506243537739, 40.08164817465998, 40.219741708422816, 38.41301797502585, 38.067784140618784, 31.51984908136483, 5.995560924202656, 0.0, 2.8194096476576793, 26.099677881173942, 38.09079972957926, 38.89634534319573, 39.86300007953551, 39.080470054879505, 39.55228962856915, 40.05863258569951, 37.688026922771016, 34.00553268909568, 24.983421816591108, 15.880756382724886, 16.663286407380895, 31.404771136562474, 29.011149884673507, 13.441103952914975, 15.949803149606298, 10.541139743895648, 0.0]],"toyplot");
    (function(axis, axis_id, projection)
            {
                axis.show_coordinates(axis_id, projection);
            })(modules["toyplot.coordinates.Axis"],"t618c0d13fcc141abb5628de92425c079",[{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 75.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 500.0, "min": 0.0}, "scale": "linear"}]);
    (function(axis, axis_id, projection)
            {
                axis.show_coordinates(axis_id, projection);
            })(modules["toyplot.coordinates.Axis"],"tf481b22bcfad4cf08c8ea85892222849",[{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 40.806639226914818, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 100.0, "min": 0.0}, "scale": "linear"}]);
    (function(tables, context_menu, io, owner_id, key, label, names, columns, filename)
            {
                tables.set(owner_id, key, names, columns);
    
                var owner = document.querySelector("#" + owner_id);
                function show_item(e)
                {
                    return owner.contains(e.target);
                }
    
                function choose_item()
                {
                    io.save_file("text/csv", "utf-8", tables.get_csv(owner_id, key), filename + ".csv");
                }
    
                context_menu.add_item("Save " + label + " as CSV", show_item, choose_item);
            })(modules["toyplot/tables"],modules["toyplot/menus/context"],modules["toyplot/io"],"t57ef92861432432e81af535b8a8612f2","data","plot data",["x", "y0"],[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75], [0.0, 2.5, 26.0, 6.0, 20.4, 88.8, 89.6, 89.4, 90.0, 91.4, 86.4, 74.5, 64.9, 67.4, 67.5, 69.8, 69.8, 69.8, 69.3, 69.5, 72.0, 70.3, 69.6, 69.6, 70.0, 73.8, 79.5, 84.7, 88.2, 88.6, 88.6, 177.5, 179.6, 193.0, 220.4, 221.8, 221.1, 221.8, 221.1, 221.5, 219.0, 216.6, 215.2, 219.0, 228.2, 239.8, 260.2, 266.1, 267.1, 254.3, 239.8, 230.7, 230.4, 230.4, 230.0, 230.0, 230.0, 230.0, 320.4, 319.9, 320.4, 320.4, 320.4, 320.4, 316.0, 294.3, 284.8, 273.1, 270.2, 334.0, 0.3, 0.1, 42.5, 67.5, 52.4, 50.3]],"toyplot");
    (function(axis, axis_id, projection)
            {
                axis.show_coordinates(axis_id, projection);
            })(modules["toyplot.coordinates.Axis"],"t424928479c104d3e9bcde462e3e9bb9a",[{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 75.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 500.0, "min": 0.0}, "scale": "linear"}]);
    (function(axis, axis_id, projection)
            {
                axis.show_coordinates(axis_id, projection);
            })(modules["toyplot.coordinates.Axis"],"tbae6e97f30cb453d987319e0d71c9465",[{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 334.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 100.0, "min": 0.0}, "scale": "linear"}]);
    })();</script></div></div>


Note that nothing prevents us from doing useful work in the ``for`` loop
that populates the cache, and nothing prevents us from accessing the
cache within the loop. For example, we might want to display field
values from individual records alongside a running average computed from
the cache. Or we might want to update our plot periodically as the loop
progresses.
