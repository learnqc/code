from math import pi

from hume import QuantumRegister, QuantumCircuit
from hume.utils.common import padded_bin


def encode_term(coeff, vars, circuit, key, value):
    for i in range(len(value)):
        if len(vars) > 1:
            # circuit.mcp(2*pi * 2 ** (i - N) * coeff, [key[j] for j in vars], value[i])
            circuit.mcp(pi * 2 ** -i * coeff, [key[j] for j in vars], value[i])
        elif len(vars) > 0:
            # circuit.cp(2*pi * 2 ** (i - N) * coeff, key[vars[0]], value[i])
            circuit.cp(pi * 2 ** -i * coeff, key[vars[0]], value[i])
        else:
            # circuit.p(2*pi * 2 ** (i - N) * coeff, value[i])
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


def poly(n_key, terms, pr=False):
    p = [0 for _ in range(2**n_key)]
    for k in range(2**n_key):
        b = padded_bin(n_key, k)
        p_k = 0
        for m in terms:
            p_k_m = m[0]
            for idx in m[1]:
                p_k_m *= int(b[n_key-1-idx])
            p_k += p_k_m
        p[k] = p_k

    if pr:
        print()
        for k in range(2**n_key):
            print(k, '=', b, '-->', p[k])

    return p
