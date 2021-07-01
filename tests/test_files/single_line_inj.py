import platform
print(platform.python_version())

import numpy as np
import matplotlib as mpl


def foo_0(bar):
    """Checking for handling of spaces on a single line."""
    return bar


def foo_1(bar):
    """ Checking for handling of spaces on a single line."""
    return bar


def foo_2(bar):
    """Checking for handling of spaces on a single line. """
    return bar


def foo_3(bar):
    """ Checking for handling of spaces on a single line. """
    return bar
