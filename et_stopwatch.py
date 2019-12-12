"""
Module et_stopwatch
===================
A context manager class for timing a piece of code.
"""

from timeit import default_timer as timer

class Stopwatch:
    """Context manager class for timing a code fragment.
    
    Usage::
    
       with Stopwatch('This took me') as sw:
           for i in range(3):
               sleep(1)
               print(i,sw.timelapse(),'s)
               
        0 1.004215 s
        1 1.003996 s
        2 1.001949 s
        This took me 3.010238 s

    :param str comment: text in front of the total time. If None nothing is printed. Default is empty str,
    :param int ndigits: number of digits after the decimal sign.
    """
    def __init__(self,message='',ndigits=6):
        self.started = -1.0
        self.stopped = -1.0
        self.message = message
        self.ndigits = ndigits

    
    def __enter__(self):
        self.start()
        return self


    def __exit__(self, exception_type, exception_value, tb):
        self.stop()
        if not self.message is None:
            print(self)

    
    #@property
    # DO NOT use the @property decorator for functions that change the state!
    def timelapse(self):
        """Return number of seconds (float) since last call to timelapse (or to start if 
        called for the first time).
        """
        now = timer()
        seconds = round(now - self.stopped,self.ndigits)
        self.stopped = now
        return seconds


    @property
    def time(self):
        """Return number of seconds between starting and stopping the stopwatch (for the last time)"""
        return round(self.stopped-self.started,self.ndigits)


    def start(self):
        """Start or restart this :py:class:`Stopwatch` object."""
        self.started = timer()
        self.stopped = self.started
    

    def stop(self):
        """Stop the :py:class:`Stopwatch` object and return the number of seconds since it was started."""
        self.stopped = timer()
        return self.time
    
    
    def __repr__(self):
        if not self.message is None:
            if not self.message.endswith(' '):
                self.message += ' '
            return self.message+'{} s'.format(self.time)
        else:
            return              '{} s'.format(self.time)

#eof