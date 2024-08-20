import random
from math import sqrt, cos, sin, pi

from hume.simulator.circuit import QuantumCircuit, QuantumRegister

from qiskit import QuantumCircuit as QC
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

from hume.utils.common import all_close


def generate_state(n, seed=555):
    # Choose a seed
    random.seed(seed)
    # Generate random probabilities that add up to 1
    probs = [random.random() for _ in range(2**n)]
    total = sum(probs)
    probs = [p / total for p in probs]
    # Generate random angles in radians
    angles = [random.uniform(0, 2 * pi) for _ in range(2**n)]
    # Build the quantum state array
    return [sqrt(p) * (cos(a) + 1j * sin(a)) for (p, a) in zip(probs, angles)]

def iqft_hume(n, targets, swap):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    state = generate_state(n)
    qc.initialize(state)
    qc.iqft(targets, swap=swap)
    state = qc.run()
    # print_state_table(state)
    return state


def iqft_qiskit(n, targets, swap):
    qc = QC(n)
    state = generate_state(n)
    qc.initialize(state)
    qft = QFT(num_qubits=len(targets), do_swaps=swap, inverse=True)
    qc.append(qft, qargs=targets)
    state = Statevector(qc).data
    # print_state_table(state)
    return state


def test_iqft_same_as_qiskit():
    for n in range(1, 10):
        targets = range(n)
        s1 = iqft_hume(n, targets, True)
        s2 = iqft_qiskit(n, targets, True)

        assert all_close(s1, s2)

        s1 = iqft_hume(n, targets, False)
        s2 = iqft_qiskit(n, targets[::-1], False) # !!! bug in Qiskit?

        assert all_close(s1, s2)


def qft_hume(n, targets, swap):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    state = generate_state(n)
    qc.initialize(state)
    qc.qft(targets, swap=swap)
    state = qc.run()
    # print_state_table(state)
    return state


def qft_qiskit(n, targets, swap):
    qc = QC(n)
    state = generate_state(n)
    qc.initialize(state)
    qft = QFT(num_qubits=len(targets), do_swaps=swap, inverse=False)
    qc.append(qft, qargs=targets)
    state = Statevector(qc).data
    # print_state_table(state)
    return state


def test_qft_same_as_qiskit():
    for n in range(1, 10):
        targets = range(n)
        s1 = qft_hume(n, targets, True)
        s2 = qft_qiskit(n, targets, True)

        assert all_close(s1, s2)

        s1 = qft_hume(n, targets, False)
        s2 = qft_qiskit(n, targets, False)

        assert all_close(s1, s2)