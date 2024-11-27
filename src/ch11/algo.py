from math import pi

from ch10.algo import *
from sim_circuit import QuantumRegister, QuantumCircuit


def encode_term(coeff, vars, circuit, key, value):
    for i in range(len(value)):
        if len(vars) > 1:
            circuit.mcp(pi * 2 ** -i * coeff, [key[j] for j in vars], value[i])
        elif len(vars) > 0:
            circuit.cp(pi * 2 ** -i * coeff, key[vars[0]], value[i])
        else:
            circuit.p(pi * 2 ** -i * coeff, value[i])


def build_polynomial_circuit(key_size, value_size, terms):
    key = QuantumRegister(key_size)
    value = QuantumRegister(value_size)
    circuit = QuantumCircuit(key, value)

    for i in range(len(key)):
        circuit.h(key[i])

    for i in range(len(value)):
        circuit.h(value[i])

    for (coeff, vars) in terms:
        encode_term(coeff, vars, circuit, key, value)

    circuit.iqft(value[::-1], swap=False)

    return circuit


def oracle_match_0(bits, tag_bit):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    qc.x(q[tag_bit])
    qc.p(pi, tag_bit)
    qc.x(q[tag_bit])

    return qc


def oracle_match_0_multi(bits, tag_bits):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    for t in tag_bits:
        qc.x(q[t])

    qc.mcp(pi, [q[t] for t in tag_bits[:-1]], q[len(q) - 1])

    for t in tag_bits:
        qc.x(q[t])

    return qc


def oracle_match_1(bits, tag_bit):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    qc.p(pi, tag_bit)

    return qc