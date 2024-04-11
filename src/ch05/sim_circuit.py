from ch04.sim_core import *
from ch03.sim_gates import *

from ch04.sim_circuit import QuantumRegister as QuantumRegister4
from ch04.sim_circuit import QuantumTransformation as QuantumTransformation4
from ch04.sim_circuit import QuantumCircuit as QuantumCircuit4

import numpy as np


class QuantumRegister(QuantumRegister4):
    pass


class QuantumTransformation(QuantumTransformation4):
    pass


class QuantumCircuit(QuantumCircuit4):

    def initialize(self, state):
        self.state = state

    def append(self, circuit, reg):
        assert(reg.size == sum(circuit.regs))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target, tr.controls, tr.name, tr.arg))

    def c_append(self, circuit, c, reg):
        assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              [c] + [reg.shift + t for t in tr.controls],
                                                              tr.name, tr.arg))
