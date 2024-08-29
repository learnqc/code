from config import SIMULATOR

if SIMULATOR == 'qiskit':
    from qiskit import QuantumRegister, QuantumCircuit
elif SIMULATOR == 'hume':
    from hume.simulator.circuit import QuantumCircuit, QuantumRegister


