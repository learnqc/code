from math import pi

from ch03.sim_gates import *
from ch06.sim_core import *

from ch06.sim_circuit import QuantumRegister as QuantumRegister6
from ch06.sim_circuit import QuantumTransformation as QuantumTransformation6
from ch06.sim_circuit import QuantumCircuit as QuantumCircuit6


class QuantumRegister(QuantumRegister6):
    pass


class QuantumTransformation(QuantumTransformation6):
    pass


class Swap:
    def __init__(self, i, j):
        self.name = 'swap'
        self.i = i
        self.j = j

    def __str__(self):
        return f'swap {self.i} {self.j}'


class QuantumCircuit(QuantumCircuit6):

    def swap(self, i, j):
        self.transformations.append(Swap(i, j))

    def mswap(self, targets):
        for j in range(len(targets) // 2):
            self.swap(targets[j], targets[len(targets)-1-j])

    def inverse(self):
        qs = [QuantumRegister(size, 'q' if len(self.regs) == 1 else None) for size in self.regs]
        qc = QuantumCircuit(*qs)

        for tr in self.transformations[::-1]:
            if isinstance(tr, Swap):
                qc.swap(tr.i, tr.j)
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
            while t >= self.regs[reg]:
                t = t - self.regs[reg]
                reg = reg + 1

            if len(cs) == 0:
                if tr.arg:
                    m(-tr.arg, qs[reg][t])
                else:
                    m(qs[reg][t])
            elif len(cs) == 1:
                if tr.arg:
                    m(-tr.arg, cs[0], qs[reg][t])
                else:
                    m(cs[0], qs[reg][t])
            # multi-control
            else:
                if tr.arg is not None:
                    m(-tr.arg, cs, qs[reg][t])
                else:
                    m(cs, qs[reg][t])

        return qc

    def run(self):
        for tr in self.transformations:
            if isinstance(tr, Swap):
                c_transform(self.state, tr.i, tr.j, x)
                c_transform(self.state, tr.j, tr.i, x)
                c_transform(self.state, tr.i, tr.j, x)

            else:
                cs = tr.controls
                if len(cs) == 0:
                    transform(self.state, tr.target, tr.gate)
                elif len(cs) == 1:
                    c_transform(self.state, cs[0], tr.target, tr.gate)
                else:
                    mc_transform(self.state, cs, tr.target, tr.gate)
        self.transformations = []
        return self.state

    def report(self, name=None):
        start_state = init_state(sum(self.regs))
        tr_count = 0
        for report in self.reports.values():
            if report[3] > tr_count:
                tr_count = report[3]
                start_state = report[2]

        qc = QuantumCircuit()
        qc.regs = self.regs.copy()
        qc.initialize(start_state.copy())
        qc.transformations = self.transformations[tr_count:].copy()
        end_state = qc.run()

        if name is None:
            name = len(self.reports)
        report = (start_state, self.transformations[tr_count:len(self.transformations)].copy(), end_state,
                  len(self.transformations))
        self.reports[name] = report
        return report

    def qft(self, targets, swap=True):
        qft(self, targets, swap)

    def append_qft(self, reg, reversed=False, swap=True):
        self.append(QFT(len(reg), reversed, swap), reg)

    def iqft(self, targets, swap=True):
        iqft(self, targets, swap)

    def append_iqft(self, reg, reversed=False, swap=True):
        self.append(IQFT(len(reg), reversed, swap), reg)

    def append(self, circuit, reg):
        assert(reg.size == sum(circuit.regs))
        for tr in circuit.transformations:
            if isinstance(tr, Swap):
                self.transformations.append(Swap(reg.shift + tr.i, reg.shift + tr.j))
                continue
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              [reg.shift + t for t in tr.controls], tr.name, tr.arg))

    def c_append(self, circuit, c, reg):
        assert(c not in range(reg.shift, reg.shift + reg.size))
        for tr in circuit.transformations:
            if isinstance(tr, Swap):
                self.transformations.append(Swap(reg.shift + tr.i, reg.shift + tr.j))
                continue
            self.transformations.append(QuantumTransformation(tr.gate, reg.shift + tr.target,
                                                              [c] + [reg.shift + t for t in tr.controls],
                                                              tr.name, tr.arg))


class QFT(QuantumCircuit):
    def __init__(self, m, reversed=False, swap=True):
        super().__init__(QuantumRegister(m))
        targets = range(m)
        if reversed:
            targets = targets[::-1]

        qft(self, targets, swap)


class IQFT(QuantumCircuit):
    def __init__(self, m, reversed=False, swap=True):
        super().__init__(QuantumRegister(m))
        targets = range(m)
        if reversed:
            targets = targets[::-1]

        iqft(self, targets, swap)


def qft(qc, targets, swap=True):
    for j in range(len(targets))[::-1]:
        qc.h(targets[j])
        for k in range(j)[::-1]:
            qc.cp(pi * 2.0 ** (k - j), targets[j], targets[k])

    if swap:
        qc.mswap(targets)


def iqft(qc, targets, swap=True):
    for j in range(len(targets))[::-1]:
        qc.h(targets[j])
        for k in range(j)[::-1]:
            qc.cp(-pi * 2 ** (k - j), targets[j], targets[k])

    if swap:
        qc.mswap(targets)
