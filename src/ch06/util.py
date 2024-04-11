import numpy as np

from ch05.util import *


def random_transformation(n):
    import scipy.stats
    U = scipy.stats.unitary_group.rvs(2**n)

    def f_direct(state):
        assert(len(state) == 2**n)
        s = U @ state
        for k in range(len(s)):
            state[k] = s[k]

    def f_inverse(state):
        assert(len(state) == 2**n)
        s = np.conj(U.transpose()) @ state
        for k in range(len(s)):
            state[k] = s[k]

    return f_direct, f_inverse


def inner(v1, v2):
    assert(len(v1) == len(v2))
    return sum(z1*z2.conjugate() for z1, z2 in zip(v1, v2))
