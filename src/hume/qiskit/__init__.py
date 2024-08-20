from collections import Counter
from random import choices

from qiskit import QuantumCircuit
from qiskit.circuit.add_control import add_control

from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector


def run(self):
    return Statevector(self).data

def c_append(self, U, c, q):
    cU = add_control(U.to_instruction(), 1, '', 0)
    self.append(cU, [c] + [qb for qb in q])


def qft(self, targets, swap=True):
    qft = QFT(num_qubits=len(targets), do_swaps=swap, inverse=False)
    self.append(qft, qargs=targets)


def iqft(self, targets, swap=True):
    iqft = QFT(num_qubits=len(targets), do_swaps=swap, inverse=True)
    self.append(iqft, qargs=targets if swap else targets[::-1])


def measure(self, shots=0):
    state = self.run()
    samples = choices(range(len(state)), [abs(state[k]) ** 2 for k in range(len(state))], k=shots)
    counts = {}
    for (k, v) in Counter(samples).items():
        counts[k] = v
    return {'state vector': state, 'counts': counts}

setattr(QuantumCircuit, 'run', run)
setattr(QuantumCircuit, 'c_append', c_append)
setattr(QuantumCircuit, 'qft', qft)
setattr(QuantumCircuit, 'iqft', iqft)
setattr(QuantumCircuit, 'measure', measure)

# QuantumCircuit.regs = property(lambda self: [len(reg) for reg in self.qregs])
