from math import pi

from ch09.algo import *
from sim_circuit import QuantumRegister, QuantumCircuit


def grover_circuit(A, O, iterations):
    n = sum(A.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(A, q)

    for i in range(1, iterations + 1):
        qc.append(grover_iterate_circuit(A, O), q)

    return qc