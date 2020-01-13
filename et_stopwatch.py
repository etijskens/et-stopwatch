"""
Module et_stopwatch
===================
A class for timing a piece of code.

Inspiration taken from `Python Timer Functions: Three Ways to Monitor Your Code <https://realpython.com/python-timer/#a-python-timer-decorator>`_

"""
__version__ = "1.0.5"

from timeit import default_timer as timer
from sys import float_info
import functools
from math import sqrt


class Stopwatch:
    """Class for timing code.

    Constructor parameters:
    
    :param str message: this text will appear when the Stopwatch object is printed
    :param int ndigits: number of digits in returned or printed timings.

    """
    def __init__(self,message='Stopwatch',ndigits=6):
        self.started = -1.0
        self.stopped = -1.0
        self.max = 0.
        self.min = float_info.max
        self.count = 0
        self.sum = 0.
        self.ssq = 0.
        self.message = message
        self.ndigits = ndigits
        self.start()

    
    def __enter__(self):
        self.start()
        return self


    def __exit__(self, exception_type, exception_value, tb):
        if self.count == 0:
            self.stop()
        print(self)

    
    def start(self,message=None):
        """Start or restart this :py:class:`Stopwatch` object.

        :param str message: modify the message used when the Stopwatch object is printed.
        """
        self.started = timer()
        self.stopped = self.started
        if message:
            self.message = message


    #@property    # NEVER use the @property decorator for functions that change the state!
    def stop(self,stats=True):
        """Stop the stopwatch.

        :param bool stats: if False no statistics are acummulated.
        :returns: the number of seconds (float) since the most recent call to stop or start.

        .. note::
            ``Stop()`` calls ``start()`` immediately before returning. This is practical in
            an iteration, but as such includes the overhead of the iteration. Call ``start()``
            explicitly to avoid this as in::

                with Stopwatch(message='This took') as sw:
                    for i in range(3):
                        sw.start()               # restart the stopwatch
                        sleep(1)                 # only this is timed
                        print(i, sw.stop(), 's') # stop the stopwatch and returns second since start

        """
        self.stopped = timer()
        t = self.stopped-self.started
        if stats:
            self.count += 1
            if t < self.min:
                self.min = t
            if t > self.max:
                self.max = t
            self.sum += t
            self.ssq += t*t
        self._time = round(t, self.ndigits)
        self.start()
        return self._time


    @property
    def time(self):
        """The number of seconds as measured in the most recent call to ``stop()``."""

        # Cannot recompute because stop() calls start() to restart the counter.
        # So recomputing it would always yield 0 s.
        return self._time


    def statistics(self):
        """Compute mean and standard deviation.

        :returns: the mean and the standard deviation.
        """
        self.mean = self.sum / self.count
        self.stddev = sqrt( (self.ssq + self.mean * (self.count * self.mean - 2. * self.sum)) / (self.count) )
        return self.mean, self.stddev


    def __repr__(self):
        """
        Print the objects message and total time. If stop was called more than once also statistics are printed
        (min, max, mean, stddev, count).
        """
        message = self.message + " : "
        if self.count <= 1:
            message += "{} s".format(self._time)
        else:
            self.statistics()
            message += "\n    total  : {} s"\
                       "\n    minimum: {} s"\
                       "\n    maximum: {} s"\
                       "\n    mean   : {} s"\
                       "\n    stddev : {} s"\
                       "\n    count  : {}"
            message = message.format(
                round(self.sum   , self.ndigits),
                round(self.min   , self.ndigits),
                round(self.max   , self.ndigits),
                round(self.mean  , self.ndigits),
                round(self.stddev, self.ndigits),
                self.count,
            )
        return message
    

    def __call__(self, func):
        """Support using StopWatch as a decorator"""
        @functools.wraps(func)
        def wrapper_stopwatch(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_stopwatch

# some use cases:
if __name__ == "__main__":

    from time import sleep

    print("# Use as class:")
    stopwatch = Stopwatch() # create and start the stopwatch
    sleep(1)
    stopwatch.stop()
    print(stopwatch)
    print(stopwatch.time)

    print()

    print("# Use as context manager:")
    with Stopwatch('This took') as sw:
        for i in range(3):
            sleep(1)
            print(i, sw.stop()) # stop() returns the time since the last call to start|stop in seconds
            print(sw.time)

    with Stopwatch('This took') as sw:
        for i in range(3):
            sw.start() # restart the Stopwatch
            sleep(1)
            print(i, sw.stop())

    print()
    print("# Use as decorator:")

    @Stopwatch(message="say_hi_and_sleep_two_seconds", ndigits=3)
    def say_hi_and_sleep_two_seconds():
        print("hi")
        sleep(2)

    say_hi_and_sleep_two_seconds()

    print("-*# done #*-")
#eof