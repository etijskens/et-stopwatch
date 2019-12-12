============
et-stopwatch
============

A context manager for timing code.

Typical use:

.. code-block:: python

    # Create a Stopwath with and end message string and printed 3 digits
    with Stopwatch("time 5 times 'sleep(1)': ",ndigits=3) as tmr:
        for i in range(5):
            sleep(1) # supposing there isn't anything more useful to oo ;-)
            print(i,tmr.timelapse()) # time since last call to timelapse()

    print(tmr.time) # the total time

Running this code yields:

.. code-block:: bash

    0 1.004
    1 1.004
    2 1.004
    3 1.004
    4 1.004
    time 5 times 'sleep(1)': 5.02 s
    5.02

* Free software: MIT license
* Documentation: https://et-stopwatch.readthedocs.io.


