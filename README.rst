=========
Datathief
=========

Small utility for retrieving data from figures. Inspired by the Java package of the same name.

To use, add a single pixel at the start and end of the x-axis (default color: pure blue) and the y-axis (default color: pure red), and then one pixel for each data point (default color: pure green). This function will then return the x and y coordinates of each data point.

For example, running this code:

.. code:: python

    import datathief as dt
    filename = 'du_fig1a_annotated.png'
    xlim = [-10, 20]
    ylim = [0, 15]
    data = dt.datathief(filename, xlim=xlim, ylim=ylim)

Extracts the data for this plot:

|Output|

See the examples folder for more information.

.. |Output| image:: examples/example-output.png