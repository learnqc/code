from math import sqrt, pi
from ch03.util import cis


def fourier_basis(N, l):
    return [1/sqrt(N) * cis(k*l*2*pi/N) for k in range(N)]
