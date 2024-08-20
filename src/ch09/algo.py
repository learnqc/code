from math import sqrt, pi

from hume.simulator.circuit import QuantumRegister, QuantumCircuit
from hume.utils.common import cis


def fourier_basis(N, l):
    return [1/sqrt(N) * cis(k*l*2*pi/N) for k in range(N)]

def uniform(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(len(q)):
        qc.h(q[i])

    return qc

def is_bit_not_set(m, k):
    return not (m & (1 << k))

def phase_oracle_match(n, items):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for m in items:
        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])

        qc.mcp(pi, [q[i] for i in range(len(q) - 1)], q[len(q) - 1])

        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])
    return qc

def inversion_0_circuit(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(n):
        qc.x(q[i])

    qc.mcp(pi, [q[i] for i in range(n - 1)], q[n - 1])

    for i in range(n):
        qc.x(q[i])

    return qc
    
def inversion_circuit(A):
    n = sum(A.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(A.inverse(), q)

    qc.append(inversion_0_circuit(n), q)

    qc.append(A, q)

    return qc

def grover_iterate_circuit(A, O):
    n = sum(O.regs)
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(O, q)

    qc.append(inversion_circuit(A), q)

    return qc
