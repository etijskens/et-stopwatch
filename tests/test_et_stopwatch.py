# -*- coding: utf-8 -*-

"""Tests for et_stopwatch package."""

from time import sleep
from contextlib import redirect_stdout
import io
from et_stopwatch import Stopwatch

def test_1():
    print("\nuse case 1: time a piece of code.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch():
            # piece of code to be timed
            sleep(1)
    s = f.getvalue()
    s0 = s.split(' ')[1]
    t = float(s0)
    assert t >= 1
    assert t < 1.01


def test_2():
    print("\nuse case 2: time a piece of code, with a message.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch("time 'sleep(1)': "):
            # piece of code to be timed
            sleep(1)
    t = float(f.getvalue().split(' ')[2])
    assert t >= 1
    assert t < 1.01

def test_3():
    print("\nuse case 3: time a piece of code, listing intermediate steps, with a message, rounding times at 3 digits.")
    f = io.StringIO()
    with redirect_stdout(f):
        with Stopwatch("time 5 times 'sleep(1)': ",ndigits=3) as tmr:
            for i in range(5):
                sleep(1)
                t = tmr.timelapse()
                print(i,t)
                assert t >= 1
                assert t < 1.01

        print(tmr.time)
        assert tmr.time >= 5
        assert tmr.time < 5.05
    s = f.getvalue()
    L5 = s.split('\n')[5]
    t = float(L5.split(' ')[4])
    assert t >= 5
    assert t < 5.05
    print(t)
    print(s)

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (otherwise all tests are normally run with pytest)
# Make sure that you run this code with the project directory as CWD, and
# that the source directory is on the path
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_3

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof