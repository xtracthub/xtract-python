import numpy as np
import matplotlib as mpl


def foo_0(bar):
    """ variety of open() calls """
    open()

    open('')

    open('dummyfile.jpg')
    
    open('dummyfile.jpg', 'wr')

    open("")

    open("dummyfile.jpg")
    
    open("dummyfile.jpg", "wr")

    with open('') as f:
        bar += 1

    with open('dummyfile.jpg') as f:
        bar += 1
    
    with open('dummyfile.jpg', 'wr') as f:
        bar += 1

    with open("") as f:
        bar += 1

    with open("dummyfile.jpg") as f:
        bar += 1
    
    with open("dummyfile.jpg", "wr") as f:
        bar += 1

    return bar


def foo_1(bar):
    """ open('') call in a docstring """
    """ open('') """
    return bar


def foo_3(bar):
    """ open('') call as a comment """
    # open('')
    return bar


def foo_4(bar):
    """ open('') call as a comment with preceding text """
    # some comment open('')
    return bar


def foo_5(bar):
    """ open('') call as a comment with succeeding text """
    # open('') some comment
    return bar


def foo_6(bar):
    """ open('') call as a comment with preceding and succeeding text """
    # first comment open('') second comment
    return bar


def foo_7(bar):
    """ open('') call as a comment with preceding and succeeding text
    across multiple lines """
    # first comment 
    # open('') 
    # second comment
    return bar


def foo_8(bar):
    """ open('') call in a docstring with preceding and succeeding text 
    across multiple lines """
    """ This is an example of something that could come up - a user makes 
    a comment that refers to a certain function i.e. open('') but clearly 
    this is not code. In this instance we do not count this as code. """
    return bar


def foo_9(bar):
    """ open('') call in a docstring with preceding text across multiple 
    lines """
    """ This is an example of something that could come up - a user makes 
    a comment that refers to a certain function i.e. open('') """
    return bar


def foo_10(bar):
    """ open('') call in a docstring with succeeding text across multiple 
    lines """
    """ open('') is a system call which makes a call to the kernenl and 
    allows the python script access to write to system files. """
    return bar

def foo_11(bar):
    """ open('') call in a docstring with preceding and succeeding text 
    across multiple lines, and odd spacing """
    """ This is an example of so
    mething 
    that could come up - a user makes 
    a comment that 
    refers to a certain     function i.e.open('')       
    but         clearly 
    this is not
        code. In this 
    instance    we do       not count this as code. """
    return bar


def foo_9(bar):
    """ open('') call in a docstring with preceding text across multiple 
    lines """
    """ This is an example of something that could come up - a user makes 
    a comment that refers to a certain function i.e. open('') """
    return bar


def foo_10(bar):
    """ open('') call in a docstring with succeeding text across multiple 
    lines """
    """ open('') is a system call which makes a call to the kernenl and 
    allows the python script access to write to system files. """
    return bar
