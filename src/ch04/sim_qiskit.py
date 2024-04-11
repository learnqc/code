from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit.quantum_info import Statevector


def run(self):
    # try:
    #     import qiskit
    #     backend = qiskit.Aer.get_backend('statevector_simulator')
    #     job = qiskit.execute(self, backend)
    # except:
    #     import qiskit_aer
    #     backend = qiskit_aer.Aer.get_backend('statevector_simulator')
    #     job = backend.run(transpile(self, backend))

    return Statevector(self)


setattr(QuantumCircuit, 'run', run)
