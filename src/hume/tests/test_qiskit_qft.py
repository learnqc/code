from hume.simulator.circuit import QuantumCircuit, QuantumRegister

from qiskit import QuantumCircuit as QC
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

from hume.utils.common import all_close, generate_state


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