from math import pi

from ch09.sim_core import *
# from sim_gates import h, phase
#
#
# def m_transform(state, targets, gate):
#     for j in targets:
#         transform(state, j, gate)
#
#
# def iqft(state, targets):
#     for j in range(len(targets))[::-1]:
#         transform(state, targets[j], h)
#         for k in range(j)[::-1]:
#             c_transform(state, targets[j], targets[k], phase(-pi * 2 ** (k - j)))
