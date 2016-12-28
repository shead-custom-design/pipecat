
.. image:: ../artwork/pipecat.png
    :width: 200px
    :align: right

.. _battery-chargers:

Battery Chargers
----------------

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    import serial
    import toyplot
    
    import pipecat.device.charger
    import pipecat.limit
    import pipecat.store
    import pipecat.utility
    
    import IPython.display

.. code:: python

    pipe = pipecat.utility.readline(serial.serial_for_url("/dev/cu.SLAB_USBtoUART", baudrate=128000))
    pipe = pipecat.device.charger.icharger208b(pipe)
    pipe = pipecat.utility.add_timestamp(pipe)
    pipe = pipecat.limit.timeout(pipe, timeout=pipecat.quantity(5, pipecat.units.seconds))
    pipe = pipecat.store.cache(pipe)
    
    for record in pipe:
        canvas = toyplot.Canvas()
        axes = canvas.cartesian(grid=(3, 1, 0), label="Battery", ylabel="Voltage (V)")
        axes.plot(pipe.table[("battery", "voltage")].to(pipecat.units.volt))
    
        axes = canvas.cartesian(grid=(3, 1, 1), ylabel="Current (A)")
        axes.plot(pipe.table[("battery", "current")].to(pipecat.units.amp))
    
        axes = canvas.cartesian(grid=(3, 1, 2), ylabel="Charge (mAH)")
        axes.plot(pipe.table[("battery", "charge")].to(pipecat.units.milliamp * pipecat.units.hour))
        
        IPython.display.clear_output()
        IPython.display.display_html(canvas)



.. raw:: html

    <div align="center" class="toyplot" id="tdde2bb9eecd345b0ae2da004770e7ade"><svg class="toyplot-canvas-Canvas" height="600px" id="tabf56e5b208b400a8febc447074d8f89" preserveAspectRatio="xMidYMid meet" style="background-color:transparent;fill:rgb(16.1%,15.3%,14.1%);fill-opacity:1.0;font-family:Helvetica;font-size:12px;opacity:1.0;stroke:rgb(16.1%,15.3%,14.1%);stroke-opacity:1.0;stroke-width:1.0" viewBox="0 0 600 600" width="600px" xmlns="http://www.w3.org/2000/svg" xmlns:toyplot="http://www.sandia.gov/toyplot" xmlns:xlink="http://www.w3.org/1999/xlink"><g class="toyplot-coordinates-Cartesian" id="tbb0b2a2842a5407a898050bda844ad2c"><clipPath id="ta6fb5fc266004ec692cc682e00ade195"><rect height="120.0" width="520.0" x="40.0" y="40.0"></rect></clipPath><g clip-path="url(#ta6fb5fc266004ec692cc682e00ade195)"><g class="toyplot-mark-Plot" id="tffc31c1f15394b2a8d03eebcfefd92d3" style="fill:none"><g class="toyplot-Series"><path d="M 50.0 150.0 L 175.0 116.6666666666716 L 300.0 50.000000000014801 L 425.0 50.000000000014801 L 550.0 50.000000000014801" style="stroke:rgb(40%,76.1%,64.7%);stroke-opacity:1.0;stroke-width:2.0"></path></g></g></g><g class="toyplot-coordinates-Axis" id="t4fbadba144764fe78355d159b3c04fbe" transform="translate(50.0,150.0)translate(0,10.0)"><line style="" x1="0" x2="500.0" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">0</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(125.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">1</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(250.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">2</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(375.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">3</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(500.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">4</tspan></text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="-3.0" y2="4.5"></line><text style="alignment-baseline:alphabetic;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="-6"></text></g></g><g class="toyplot-coordinates-Axis" id="t751bb88ff41345169450093d1bf964e3" transform="translate(50.0,150.0)rotate(-90.0)translate(0,-10.0)"><line style="" x1="0" x2="99.9999999999852" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,-6)"><tspan style="font-size:10.0px">3.874</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(33.3333333333284,-6)"><tspan style="font-size:10.0px">3.875</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(66.6666666666568,-6)"><tspan style="font-size:10.0px">3.876</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(100.0,-6)"><tspan style="font-size:10.0px">3.877</tspan></text></g><text style="font-weight:bold;stroke:none;text-anchor:middle" transform="translate(50.0,-22)"><tspan style="font-size:12.0px">Voltage (V)</tspan></text><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="3.0" y2="-4.5"></line><text style="alignment-baseline:hanging;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="6"></text></g></g><text style="font-weight:bold;stroke:none;text-anchor:middle" transform="translate(300.0,50.0)translate(0,-10.0625)"><tspan style="font-size:14.0px">Battery</tspan></text></g><g class="toyplot-coordinates-Cartesian" id="t6f716ad87d0a406b9f03b86d2cb34e66"><clipPath id="t8a91eae7adfe4347a69f22cdc16fdb52"><rect height="120.0" width="520.0" x="40.0" y="240.0"></rect></clipPath><g clip-path="url(#t8a91eae7adfe4347a69f22cdc16fdb52)"><g class="toyplot-mark-Plot" id="t9ea28af1f91143d48fc0985e518973ce" style="fill:none"><g class="toyplot-Series"><path d="M 50.0 250.0 L 175.0 275.0 L 300.0 350.0 L 425.0 325.0 L 550.0 325.0" style="stroke:rgb(40%,76.1%,64.7%);stroke-opacity:1.0;stroke-width:2.0"></path></g></g></g><g class="toyplot-coordinates-Axis" id="t84a70b0e23f846bc92d01a5b196ca672" transform="translate(50.0,350.0)translate(0,10.0)"><line style="" x1="0" x2="500.0" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">0</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(125.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">1</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(250.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">2</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(375.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">3</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(500.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">4</tspan></text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="-3.0" y2="4.5"></line><text style="alignment-baseline:alphabetic;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="-6"></text></g></g><g class="toyplot-coordinates-Axis" id="t427e989eb4874304aa7aa7a922b2b736" transform="translate(50.0,350.0)rotate(-90.0)translate(0,-10.0)"><line style="" x1="0" x2="100.0" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,-6)"><tspan style="font-size:10.0px">0.89</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(25.0,-6)"><tspan style="font-size:10.0px">0.90</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(50.0,-6)"><tspan style="font-size:10.0px">0.91</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(75.0,-6)"><tspan style="font-size:10.0px">0.92</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(100.0,-6)"><tspan style="font-size:10.0px">0.93</tspan></text></g><text style="font-weight:bold;stroke:none;text-anchor:middle" transform="translate(50.0,-22)"><tspan style="font-size:12.0px">Current (A)</tspan></text><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="3.0" y2="-4.5"></line><text style="alignment-baseline:hanging;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="6"></text></g></g></g><g class="toyplot-coordinates-Cartesian" id="tf21680f1c65341ea90b517178f691110"><clipPath id="t3fa2354a2c6c4464a8e7efc7c9b9e13f"><rect height="120.0" width="520.0" x="40.0" y="440.0"></rect></clipPath><g clip-path="url(#t3fa2354a2c6c4464a8e7efc7c9b9e13f)"><g class="toyplot-mark-Plot" id="t1d397e63547d4cb7947dd918408ad923" style="fill:none"><g class="toyplot-Series"><path d="M 50.0 550.0 L 175.0 550.0 L 300.0 500.0 L 425.0 500.0 L 550.0 450.0" style="stroke:rgb(40%,76.1%,64.7%);stroke-opacity:1.0;stroke-width:2.0"></path></g></g></g><g class="toyplot-coordinates-Axis" id="t913da0528be947c0a6578984f0a12437" transform="translate(50.0,550.0)translate(0,10.0)"><line style="" x1="0" x2="500.0" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">0</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(125.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">1</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(250.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">2</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(375.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">3</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(500.0,6)translate(0,7.5)"><tspan style="font-size:10.0px">4</tspan></text></g><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="-3.0" y2="4.5"></line><text style="alignment-baseline:alphabetic;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="-6"></text></g></g><g class="toyplot-coordinates-Axis" id="t7a44307dd4d344f199aab834a0999b41" transform="translate(50.0,550.0)rotate(-90.0)translate(0,-10.0)"><line style="" x1="0" x2="100.0" y1="0" y2="0"></line><g><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(0.0,-6)"><tspan style="font-size:10.0px">0.0</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(25.0,-6)"><tspan style="font-size:10.0px">0.5</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(50.0,-6)"><tspan style="font-size:10.0px">1.0</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(75.0,-6)"><tspan style="font-size:10.0px">1.5</tspan></text><text style="font-weight:normal;stroke:none;text-anchor:middle" transform="translate(100.0,-6)"><tspan style="font-size:10.0px">2.0</tspan></text></g><text style="font-weight:bold;stroke:none;text-anchor:middle" transform="translate(50.0,-22)"><tspan style="font-size:12.0px">Charge (mAH)</tspan></text><g class="toyplot-coordinates-Axis-coordinates" style="visibility:hidden" transform=""><line style="stroke:rgb(43.9%,50.2%,56.5%);stroke-opacity:1.0;stroke-width:1.0" x1="0" x2="0" y1="3.0" y2="-4.5"></line><text style="alignment-baseline:hanging;fill:rgb(43.9%,50.2%,56.5%);fill-opacity:1.0;font-size:10px;font-weight:normal;stroke:none;text-anchor:middle" x="0" y="6"></text></g></g></g></svg><div class="toyplot-interactive"><ul class="toyplot-mark-popup" onmouseleave="this.style.visibility='hidden'" style="background:rgba(0%,0%,0%,0.75);border:0;border-radius:6px;color:white;cursor:default;list-style:none;margin:0;padding:5px;position:fixed;visibility:hidden">
                <li class="toyplot-mark-popup-title" style="color:lightgray;cursor:default;padding:5px;list-style:none;margin:0"></li>
                <li class="toyplot-mark-popup-save-csv" onmouseout="this.style.color='white';this.style.background='steelblue'" onmouseover="this.style.color='steelblue';this.style.background='white'" style="border-radius:3px;padding:5px;list-style:none;margin:0">
                    Save as .csv
                </li>
            </ul><script>
            (function()
            {
              var data_tables = [{"title": "Plot Data", "names": ["x", "y0"], "id": "tffc31c1f15394b2a8d03eebcfefd92d3", "columns": [[0, 1, 2, 3, 4], [3.874, 3.875, 3.877, 3.877, 3.877]], "filename": "toyplot"}, {"title": "Plot Data", "names": ["x", "y0"], "id": "t9ea28af1f91143d48fc0985e518973ce", "columns": [[0, 1, 2, 3, 4], [0.93, 0.92, 0.89, 0.9, 0.9]], "filename": "toyplot"}, {"title": "Plot Data", "names": ["x", "y0"], "id": "t1d397e63547d4cb7947dd918408ad923", "columns": [[0, 1, 2, 3, 4], [0.0, 0.0, 1.0, 1.0, 2.0]], "filename": "toyplot"}];
    
              function save_csv(data_table)
              {
                var uri = "data:text/csv;charset=utf-8,";
                uri += data_table.names.join(",") + "\n";
                for(var i = 0; i != data_table.columns[0].length; ++i)
                {
                  for(var j = 0; j != data_table.columns.length; ++j)
                  {
                    if(j)
                      uri += ",";
                    uri += data_table.columns[j][i];
                  }
                  uri += "\n";
                }
                uri = encodeURI(uri);
    
                var link = document.createElement("a");
                if(typeof link.download != "undefined")
                {
                  link.href = uri;
                  link.style = "visibility:hidden";
                  link.download = data_table.filename + ".csv";
    
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }
                else
                {
                  window.open(uri);
                }
              }
    
              function open_popup(data_table)
              {
                return function(e)
                {
                  var popup = document.querySelector("#tdde2bb9eecd345b0ae2da004770e7ade .toyplot-mark-popup");
                  popup.querySelector(".toyplot-mark-popup-title").innerHTML = data_table.title;
                  popup.querySelector(".toyplot-mark-popup-save-csv").onclick = function() { popup.style.visibility = "hidden"; save_csv(data_table); }
                  popup.style.left = (e.clientX - 50) + "px";
                  popup.style.top = (e.clientY - 20) + "px";
                  popup.style.visibility = "visible";
                  e.stopPropagation();
                  e.preventDefault();
                }
    
              }
    
              for(var i = 0; i != data_tables.length; ++i)
              {
                var data_table = data_tables[i];
                var event_target = document.querySelector("#" + data_table.id);
                event_target.oncontextmenu = open_popup(data_table);
              }
            })();
            </script><script>
            (function()
            {
                function _sign(x)
                {
                    return x < 0 ? -1 : x > 0 ? 1 : 0;
                }
    
                function _mix(a, b, amount)
                {
                    return ((1.0 - amount) * a) + (amount * b);
                }
    
                function _log(x, base)
                {
                    return Math.log(Math.abs(x)) / Math.log(base);
                }
    
                function _in_range(a, x, b)
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
                        if(_in_range(segment.range.min, range, segment.range.max))
                            return true;
                    }
                    return false;
                }
    
                function to_domain(range, projection)
                {
                    for(var i = 0; i != projection.length; ++i)
                    {
                        var segment = projection[i];
                        if(_in_range(segment.range.bounds.min, range, segment.range.bounds.max))
                        {
                            if(segment.scale == "linear")
                            {
                                var amount = (range - segment.range.min) / (segment.range.max - segment.range.min);
                                return _mix(segment.domain.min, segment.domain.max, amount)
                            }
                            else if(segment.scale[0] == "log")
                            {
                                var amount = (range - segment.range.min) / (segment.range.max - segment.range.min);
                                var base = segment.scale[1];
                                return _sign(segment.domain.min) * Math.pow(base, _mix(_log(segment.domain.min, base), _log(segment.domain.max, base), amount));
                            }
                        }
                    }
                }
    
                function display_coordinates(e)
                {
                    var current = svg.createSVGPoint();
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
    
                var root_id = "tdde2bb9eecd345b0ae2da004770e7ade";
                var axes = {"t427e989eb4874304aa7aa7a922b2b736": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 0.93000000000000005, "min": 0.89000000000000001}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 100.0, "min": 0.0}, "scale": "linear"}], "t4fbadba144764fe78355d159b3c04fbe": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 4.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 500.0, "min": 0.0}, "scale": "linear"}], "t751bb88ff41345169450093d1bf964e3": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 3.8770000000000002, "min": 3.8740000000000001}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 100.0, "min": 0.0}, "scale": "linear"}], "t7a44307dd4d344f199aab834a0999b41": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 2.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 100.0, "min": 0.0}, "scale": "linear"}], "t84a70b0e23f846bc92d01a5b196ca672": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 4.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 500.0, "min": 0.0}, "scale": "linear"}], "t913da0528be947c0a6578984f0a12437": [{"domain": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 4.0, "min": 0.0}, "range": {"bounds": {"max": Infinity, "min": -Infinity}, "max": 500.0, "min": 0.0}, "scale": "linear"}]};
    
                var svg = document.querySelector("#" + root_id + " svg");
                svg.addEventListener("click", display_coordinates);
            })();
            </script></div></div>

