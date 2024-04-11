from ch09.sim_core import *
from ch03.sim_gates import *
from ch09.util import *

from ch08.sim_circuit import QuantumRegister as QuantumRegister8
from ch08.sim_circuit import QuantumTransformation as QuantumTransformation8
from ch08.sim_circuit import QuantumCircuit as QuantumCircuit8
from ch07.sim_circuit import Swap

import numpy as np


class QuantumRegister(QuantumRegister8):
    pass


class QuantumTransformation(QuantumTransformation8):
    pass


class QuantumCircuit(QuantumCircuit8):

    def unitary(self, U, t):
        self.transformations.append(QuantumTransformation(U, t, [], 'unitary'))

    def append_u(self, U, q):
        assert(U.shape[0] == U.shape[1] == 2**q.size)
        self.unitary(U, q.shift)

    def c_unitary(self, U, c, t):
        self.transformations.append(QuantumTransformation(U, t, [c], 'unitary'))

    def c_append_u(self, U, c, q):
        assert(U.shape[0] == U.shape[1] == 2**q.size)
        self.c_unitary(U, c, q.shift)

    def run(self):
        for tr in self.transformations:
            if tr.name == 'unitary':
                cs = tr.controls
                if len(cs) == 0:
                    transform_u(self.state, tr.gate, tr.target)
                elif len(cs) == 1:
                    c_transform_u(self.state, tr.gate, cs[0], tr.target)

            elif isinstance(tr, Swap):
                c_transform(self.state, tr.i, tr.j, x)
                c_transform(self.state, tr.j, tr.i, x)
                c_transform(self.state, tr.i, tr.j, x)

            else:
                cs = tr.controls
                if len(cs) == 0:
                    transform(self.state, tr.target, tr.gate)
                elif len(cs) == 1:
                    c_transform(self.state, cs[0], tr.target, tr.gate)
                else:
                    mc_transform(self.state, cs, tr.target, tr.gate)
        self.transformations = []
        return self.state

    def inverse(self):
        qs = [QuantumRegister(size, 'q' if len(self.regs) == 1 else None) for size in self.regs]
        qc = QuantumCircuit(*qs)

        for tr in self.transformations[::-1]:
            if isinstance(tr, Swap):
                qc.swap(tr.i, tr.j)
                continue

            if tr.name == 'unitary':
                cs = tr.controls
                if len(cs) == 0:
                    qc.unitary(dagger(tr.gate), tr.target)
                    continue
                elif len(cs) == 1:
                    qc.c_unitary(dagger(tr.gate), cs[0], tr.target)
                    continue

            prefix = ''
            if len(tr.controls) == 1:
                prefix = 'c'
            elif len(tr.controls) > 1:
                prefix = 'mc'

            m = getattr(qc, prefix + tr.name)
            cs = tr.controls

            t = tr.target
            reg = 0
            while t >= self.regs[reg]:
                t = t - self.regs[reg]
                reg = reg + 1

            if len(cs) == 0:
                if tr.arg:
                    m(-tr.arg, qs[reg][t])
                else:
                    m(qs[reg][t])
            elif len(cs) == 1:
                if tr.arg:
                    m(-tr.arg, cs[0], qs[reg][t])
                else:
                    m(cs[0], qs[reg][t])

        return qc
