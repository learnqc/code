from math import cos, sin, sqrt

x = [[0, 1], [1, 0]]

z = [[1, 0], [0, -1]]


def phase(theta):
    return [[1, 0], [0, complex(cos(theta), sin(theta))]]


h = [[1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]]


def rz(theta):
    return [[complex(cos(theta / 2), -sin(theta / 2)), 0], [0, complex(cos(theta / 2), sin(theta / 2))]]


y = [[0, complex(0, -1)], [complex(0, 1), 0]]


def rx(theta):
    return [[cos(theta / 2), complex(0, -sin(theta / 2))], [complex(0, -sin(theta / 2)), cos(theta / 2)]]


def ry(theta):
    return [[cos(theta / 2), -sin(theta / 2)], [sin(theta / 2), cos(theta / 2)]]
