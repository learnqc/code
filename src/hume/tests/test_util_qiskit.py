from math import pi

from hume.simulator.circuit import QuantumCircuit, QuantumRegister
from hume.qiskit.util import same_as_qiskit, hume_to_qiskit


def encode_value_q(n, v):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for j in range(n):
        qc.h(q[j])

    for j in range(n):
        qc.p(2 * pi / 2 ** (n - j) * v, q[j])
        # qc.p(2 * pi / 2 ** (j + 1) * v, q[j]) # version 2

    qc.report('geometric_sequence')

    qc.append_iqft(q)
    # qc.iqft(range(n)[::-1], swap=False) # version 2

    qc.report('iqft')

    return qc


def test_same_as_qiskit():
    qc = encode_value_q(3, 4.7)
    print(hume_to_qiskit(qc.regs, qc.transformations))
    same_as_qiskit(qc)


if __name__ == "__main__":
    test_same_as_qiskit()
