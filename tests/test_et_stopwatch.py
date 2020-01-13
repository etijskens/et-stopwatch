# -*- coding: utf-8 -*-

"""Tests for et_stopwatch package."""

from time import sleep
from contextlib import redirect_stdout
import io
import numpy as np
import math
from et_stopwatch import Stopwatch

def test_class_1():
    ta = []
    stopwatch = Stopwatch(name='my timer')
    sleep(1)
    t = stopwatch.stop()
    print(t)
    assert t >= 1
    assert t < 1.01
    assert stopwatch.count == 1
    print(stopwatch)
    ta.append(t)

    sleep(1)
    t = stopwatch.stop()
    print(t)
    assert t >= 1
    assert t < 1.01
    assert stopwatch.count == 2
    ta.append(t)
    print(stopwatch)

    mean = np.mean(ta)
    stddev = np.std(ta)
    # print(mean,stddev)
    assert math.isclose(mean, stopwatch.mean, abs_tol=1.0e-6)
    assert math.isclose(stddev, stopwatch.stddev, abs_tol=1.0e-6)

def test_context_manager_1():
    print("\nuse case 1: time a piece of code.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch():
            # piece of code to be timed
            sleep(1)
    s = f.getvalue()
    s = s.split(' ')
    s0 = s[2]
    t = float(s0)
    assert t >= 1
    assert t < 1.01


def test_context_manager_2():
    print("\nuse case 2: time a piece of code, with a message.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch("time 'sleep(1)'"):
            # piece of code to be timed
            sleep(1)
    s = f.getvalue()
    print(s)
    t = float(s.split(' ')[3])
    assert t >= 1
    assert t < 1.01

def test_context_manager_3():
    print("\nuse case 3: time a piece of code, listing intermediate steps, with a message, rounding times at 3 digits.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch("time 5 times 'sleep(1)': ",ndigits=3) as tmr:
            for i in range(5):
                sleep(1)
                t = tmr.stop()
                print(i,t)
                assert t >= 1
                assert t < 1.01

        print(tmr)
        assert tmr.sum >= 5
        assert tmr.sum < 5.05
        assert tmr.count == 5


def test_decorator_1():
    @Stopwatch('my timer')
    def mysleep():
        print("hi")
        sleep(1)
    mysleep()


# ==============================================================================
# The code below is for debugging a particular test.
# (otherwise all tests are normally run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_decorator_1

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof