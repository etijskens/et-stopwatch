============
et-stopwatch
============

A class for timing code. A Stopwatch object can be used to time code using its ``start`` and
``stop`` methods::

    from et_stopwatch import Stopwatch

    stopwatch = Stopwatch() # create and start the stopwatch
    sleep(1)
    stopwatch.stop()
    print(stopwatch)

    stopwatch : 1.003744 s

Use as a **context manager**::

    with Stopwatch(message='This took') as sw: # using a custom message
        for i in range(3):
            sleep(1)
            print(i, sw.stop(), 's') # stop() returns the time since the last call to start|stop in seconds

    0 1.004943
    1 1.004948
    2 1.003404
    This took :
        total  : 3.0132949999999994 s
        minimum: 1.003404 s
        maximum: 1.004948 s
        mean   : 1.004432 s
        stddev : 0.000727 s
        count  : 3

Since stop was called more than once, some statistics are printed.
Use as a **decorator**::

    @Stopwatch(name="say_hi_and_sleep_two_seconds", ndigits=3) # custom message, print only 3 digits.
    def say_hi_and_sleep_two_seconds():
        print("hi")
        sleep(2)

    say_hi_and_sleep_two_seconds()

    hi
    say_hi_and_sleep_two_seconds : 2.003 s

* Free software: MIT license
* Documentation: https://et-stopwatch.readthedocs.io.


