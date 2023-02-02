"""
Module et_stopwatch
===================
A class for timing a piece of code.

Inspiration taken from `Python Timer Functions: Three Ways to Monitor Your Code <https://realpython.com/python-timer/#a-python-timer-decorator>`_

"""
__version__ = "1.2.1"

from timeit import default_timer as timer
from sys import float_info, stdout
from datetime import datetime
import functools
from math import sqrt
from pathlib import Path
import pickle

class Statistics:
    def __init__(self, ndigits=3):
        self.max = 0.
        self.min = float_info.max
        self.count = 0
        self.sum = 0.
        self.ssq = 0.
        self.ndigits = ndigits

    def __call__(self, t):
        self.count += 1
        if t < self.min:
            self.min = t
        if t > self.max:
            self.max = t
        self.sum += t
        self.ssq += t * t

    def __repr__(self):
        if self.count > 1:
            self.mean = self.sum / self.count
            self.stddev = sqrt( (self.ssq + self.mean * (self.count * self.mean - 2. * self.sum)) / (self.count) )
            s = f"\n    total  : {round(self.sum,    self.ndigits)} s" \
                f"\n    minimum: {round(self.min,    self.ndigits)} s" \
                f"\n    maximum: {round(self.max,    self.ndigits)} s" \
                f"\n    mean   : {round(self.mean,   self.ndigits)} s" \
                f"\n    stddev : {round(self.stddev, self.ndigits)} s" \
                f"\n    count  : {self.count}" 
        else:
            s = f"{round(self.sum, self.ndigits)} s"

        return s

# Caveat: sending the output to a file (or file-like object)
# Some thoughts...
# 1 In a single threaded setting, it is best to keep the file open, as opening
#   and closing causes overhead.
# 2 In a multi-threaded (or multi-process) setting, this is not possible. If one
#   thread or process opens the file, the other cannot access it. Consequently,
#   one must keep one file per thread or process, or write atomically (i.e. open,
#   the file, write to it and close the file again). The latter is bad for parallel
#   file systems (many small write operations).

class Stopwatch:
    """Class for timing code.

    Constructor parameters:
    
    :param str message: this text will appear when the Stopwatch object is printed
    :param int ndigits: number of digits in returned or printed timings.

    """
    def __init__(self, message='Stopwatch', ndigits=6, file=stdout):
        """

        :param message:
        :param ndigits:
        :param file: filename, file handle, or file-like object. If it is a filename
            (str), the writes are managed atomically, i.e. the file is opened (with mode='a'),
            written to and closed again.
        """
        self.started = -1.0
        self.stopped = -1.0
        self.stats = Statistics(ndigits)
        self.message = message
        if isinstance(file, str):
            self.filename = file
            self.file = None
        else:
            self.filename = None
            self.file = file
        self.start()

    
    def __enter__(self):
        self.start()
        return self


    def __exit__(self, exception_type, exception_value, tb):
        if self.stats.count == 0:
            self.stop()

        if not self.file:
            self.file = open(self.filename, mode='a')

        if self.filename:
            # print statistics to a separate file.
            t = self.stats.sum
            p = Path(f'{self.filename}.stats')
            if p.is_file():
                with p.open(mode='rb') as fp:
                    stats = pickle.load(fp)
            else:
                stats = Statistics(self.stats.ndigits)
            stats(self.stats.sum)
            with p.open(mode='wb') as fp:
                pickle.dump(stats,fp)
            if stats.count > 1:
                print('Overview:',stats, file=self.file)

    
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
        self.stats(t)
        self._time = round(t, self.stats.ndigits)
        self.start()
        return self._time


    @property
    def time(self):
        """The number of seconds as measured in the most recent call to ``stop()``."""

        # Cannot recompute because stop() calls start() to restart the counter.
        # So recomputing it would always yield 0 s.
        return self._time


    def __repr__(self):
        """
        Print the objects message and total time. If stop was called more than once also statistics are printed
        (min, max, mean, stddev, count).
        """
        return f"{self.message} : " + str(self.stats)


    def __call__(self, func):
        """Support using StopWatch as a decorator"""
        @functools.wraps(func)
        def wrapper_stopwatch(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_stopwatch

    # def __del__(self):
    #     if not self.file == stdout:
    #         print(f'{self.message} destroyed: {datetime.now()}', file=self.file)
    #         self.file.close()
    #         with open(self.filename) as f:
    #             lines = list(f)
    #         # for line in lines:




# some use cases:
if __name__ == "__main__":

    from time import sleep

    print("# Use as class:")
    stopwatch = Stopwatch() # create and start the stopwatch
    sleep(1)
    stopwatch.stop()
    print(stopwatch)
    print(stopwatch.time)

    stopwatch = Stopwatch(file='test.txt') # create and start the stopwatch
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

    for p in ['test.txt', 'test.txt.stats']:
        Path(p).unlink()

    with Stopwatch('This took', file='test.txt') as sw:
        for i in range(3):
            sw.start() # restart the Stopwatch
            sleep(1)
            print(i, sw.stop())

    with Stopwatch('This took', file='test.txt') as sw:
        for i in range(4):
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