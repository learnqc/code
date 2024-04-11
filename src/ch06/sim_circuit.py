from ch04.sim_core import *

from ch05.sim_circuit import QuantumRegister as QuantumRegister5
from ch05.sim_circuit import QuantumTransformation as QuantumTransformation5
from ch05.sim_circuit import QuantumCircuit as QuantumCircuit5


class QuantumRegister(QuantumRegister5):
    pass


class QuantumTransformation(QuantumTransformation5):
    pass


class QuantumCircuit(QuantumCircuit5):

    def inverse(self):
        qs = [QuantumRegister(size, 'q' if len(self.regs) == 1 else None) for size in self.regs]
        qc = QuantumCircuit(*qs)

        for tr in self.transformations[::-1]:
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

        return qc

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
