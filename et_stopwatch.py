"""
Module et_stopwatch
===================
A class for timing a piece of code.
"""
__version__ = "0.2.1"

from timeit import default_timer as timer
from sys import float_info
import functools
from math import sqrt


class Stopwatch:
    """Class for timing code.

    Use as class::

        stopwatch = Stopwatch()
        sleep(1)
        stopwatch.stop()
        print(stopwatch)

        >>> stopwatch : 1.003744 s

    Use as context manager::

        with Stopwatch('This took') as sw:
            for i in range(3):
                sleep(1)
                print(i, sw.stop())

        0 1.004194
        1 1.003886
        2 1.000814
        This took :
            total  : 3.008894 s
            minimum: 1.000814 s
            maximum: 1.004194 s
            mean   : 1.002965 s
            stddev : 0.001526 s
            count  : 3

    Use as decorator::

        @Stopwatch(name="say_hi_and_sleep_two_seconds", ndigits=3)
        def say_hi_and_sleep_two_seconds():
            print("hi")
            sleep(2)

        say_hi_and_sleep_two_seconds()

        hi
        say_hi_and_sleep_two_seconds : 2.003 s

    Constructor parameters:
    
    :param str name: text in front of the total time. If None nothing is printed. Default is empty str,
    :param int ndigits: number of printed decimal digits in printed timings.

    Inspiration taken from `RealPython Python Timer Functions: Three Ways to Monitor Your Code <https://realpython.com/python-timer/#a-python-timer-decorator>`_
    """
    def __init__(self,name='Stopwatch',ndigits=6):
        self.started = -1.0
        self.stopped = -1.0
        self.max = 0.
        self.min = float_info.max
        self.count = 0
        self.sum = 0.
        self.ssq = 0.
        self.name = name
        self.ndigits = ndigits
        self.start()

    
    def __enter__(self):
        self.start()
        return self


    def __exit__(self, exception_type, exception_value, tb):
        if self.count == 0:
            self.stop()
        print(self)

    
    def start(self):
        """Start or restart this :py:class:`Stopwatch` object."""
        self.started = timer()
        self.stopped = self.started


    #@property    # NEVER use the @property decorator for functions that change the state!
    def stop(self):
        """Stop the stopwatch and return number of seconds (float) since the latest call to stop or start.
        """
        self.stopped = timer()
        self.count += 1
        t = self.time
        if t < self.min:
            self.min = t
        if t > self.max:
            self.max = t
        self.sum += t
        self.ssq += t*t
        self.start()
        self.last = t
        return t


    @property
    def time(self):
        """Return number of seconds between the latest start and stop the :py:class:`Stopwatch`."""
        return round(self.stopped-self.started, self.ndigits)


    def statistics(self):
        """Compute mean and standard deviation."""
        self.mean = round(self.sum / self.count, self.ndigits)
        self.stddev = round(sqrt( (self.ssq + self.mean * (self.count * self.mean - 2. * self.sum)) / (self.count) ), self.ndigits)
        return self.mean, self.stddev


    def __repr__(self):
        """
        Print the objects name and total time. If stop was called more than once also statistics are printed
        (min, max, mean, stddev, count).
        """
        message = self.name + " : "
        if self.count == 1:
            message += "{} s".format(self.last)
        else:
            mean, stddev = self.statistics()
            message += "\n    total  : {} s"\
                       "\n    minimum: {} s"\
                       "\n    maximum: {} s"\
                       "\n    mean   : {} s"\
                       "\n    stddev : {} s"\
                       "\n    count  : {}"
            message = message.format(self.sum, self.min, self.max, mean, stddev, self.count)
        return message
    

    def __call__(self, func):
        """Support using StopWatch as a decorator"""
        @functools.wraps(func)
        def wrapper_stopwatch(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_stopwatch

if __name__ == "__main__":
    """some use cases"""
    from time import sleep
    print("# Use as class:")
    stopwatch = Stopwatch()
    sleep(1)
    stopwatch.stop()
    print(stopwatch)

    print()

    print("# Use as context manager:")
    with Stopwatch('This took') as sw:
        for i in range(3):
            sleep(1)
            print(i, sw.stop())

    print()
    print("# Use as decorator:")

    @Stopwatch(name="say_hi_and_sleep_two_seconds", ndigits=3)
    def say_hi_and_sleep_two_seconds():
        print("hi")
        sleep(2)

    say_hi_and_sleep_two_seconds()

    print("-*# done #*-")
#eof