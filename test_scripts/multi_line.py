import numpy as np
import matplotlib as mpl

def foo_0(bar):
    """Checking for handling of 
    spaces on a double line."""
    return bar


def foo_1(bar):
    """ Checking for handling
    of spaces on a double line. """
    return bar


def foo_2(bar):
    """ Checking
    for
    handling
    of
    spaces
    on
    a
    double
    line. """
    return bar


def foo_3(bar):
    """ Checking    for handling    of
        spaces  on  a   double  line. """
    return bar


def foo_4(bar):
    """ Checking    for
    handling
    of
        spaces
        on  a
        double  line. """
    return bar
