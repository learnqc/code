from ch07.util import *


def prod(iterable):
    p = 1
    for n in iterable:
        p *= n
    return p
