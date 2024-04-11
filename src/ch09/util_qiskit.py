from math import log2

from ch07.sim_circuit import Swap
from ch07.util import print_state_table, all_close

from ch04.sim_qiskit import *
from ch08.util_qiskit import *


def hume_to_qiskit(regs, transformations):
    qs = [QuantumRegister(size, 'q' if len(regs) == 1 else None) for size in regs]
    qc = QuantumCircuit(*qs)

    for tr in transformations:
        if isinstance(tr, Swap):
            qc.swap(tr.i, tr.j)
            continue
        if tr.name == 'unitary':
            U = tr.gate
            assert(U.shape[0] == U.shape[1])
            m = int(log2(U.shape[0]))
            qc.unitary(U, [i + tr.target for i in range(m)])
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
        while t >= regs[reg]:
            t = t - regs[reg]
            reg = reg + 1

        if len(cs) == 0:
            if tr.arg is None:
                m(qs[reg][t])
            else:
                m(tr.arg, qs[reg][t])
        elif len(cs) == 1:
            if tr.arg:
                m(tr.arg, cs[0], qs[reg][t])
            else:
                m(cs[0], qs[reg][t])
        else:
            if tr.arg:
                m(tr.arg, cs, qs[reg][t])
            else:
                m(cs, qs[reg][t])

    return qc


def same_as_qiskit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return all_close(qc.run(), qc_qiskit.run())


def print_circuit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    print(qc_qiskit)


def draw_circuit(qc, format='mpl'):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return qc_qiskit.draw(format)


def same_as_qiskit(qc):
    qc_qiskit = hume_to_qiskit(qc.regs, qc.transformations)
    return all_close(qc.run(), as_array(qc_qiskit.run()))
