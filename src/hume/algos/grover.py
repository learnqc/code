from math import log2, sin, asin, sqrt, pi, cos

from hume import QuantumRegister, QuantumCircuit
from hume.simulator.core import transform, init_state
from hume.simulator.gates import h, ry
from hume.utils.common import inner, is_close, padded_bin
from hume.utils.matrix import dagger


def inversion_with_inversion_0_uniform(state):
    n = int(log2(len(state)))
    for j in range(n):
        transform(state, j, h)

    state[0] *= -1
    for j in range(n):
        transform(state, j, h)

    # negative sign in theory
    for k in range(len(state)):
        state[k] *= -1


def inversion_with_inversion_0_binomial(state, phi):
    n = int(log2(len(state)))
    for j in range(n):
        transform(state, j, ry(-phi))

    state[0] *= -1
    for j in range(n):
        transform(state, j, ry(phi))

    for k in range(len(state)):
        state[k] *= -1


def oracle(state, predicate):
    for item in range(len(state)):
        if predicate(item):
            state[item] *= -1


def inversion(original, current):
    proj = inner(original, current)
    for k in range(len(current)):
        current[k] = 2 * proj * original[k] - current[k]
        # assert is_close((original[k]*current[k].conjugate()).imag, 0) # in Grover iterate


def inversion_by_the_mean_direct(s, state):
    mean = 1 / len(state) * sum(z for z in state)
    # print('\nmean', mean)
    proj = inner(s, state)

    for k in range(len(state)):
        # assert is_close(mean, proj*s[k])
        # state[k] = 2*proj*s[k] - state[k] # projection formula
        state[k] = 2 * mean - state[k]


def grover_sim(state, predicate, iterations, phi=0):
    s = state.copy()

    # N = len(state)
    # count = [predicate(k) for k in range(N)].count(True)
    # theta = asin(sqrt(count/N))
    # p = 0
    # for item in range(len(state)):
    #     if predicate(item):
    #         p += abs(state[item])**2

    p = sum(abs(state[k]) ** 2 for k in range(len(state)) if predicate(k))
    theta = asin(sqrt(p))
    assert is_close(inner(s, state), 1)

    # Grover iterate
    for it in range(1, iterations + 1):
        # oracle (reflection in bad state vector)
        oracle(state, predicate)

        # inversion (reflection in original state)
        inversion(s, state)
        # inversion_by_the_mean_direct(s, state) # works for uniform

        # alternative inversion
        # inversion_with_inversion_0_uniform(state)
        # inversion_with_inversion_0_binomial(state, phi)
        # print(f'iteration {it}', inner(s, state), cos(2*it*theta))
        assert is_close(inner(s, state), cos(2 * it * theta))

        p = sum(abs(state[k]) ** 2 for k in range(len(state)) if predicate(k))
        assert is_close(p, sin((2 * it + 1) * theta) ** 2)


def inversion_0_transformation(f, state):
    n = int(log2(len(state)))

    transform = f[0]  # TODO
    inverse_transform = f[1]

    inverse_transform(state)
    inversion(init_state(n), state)
    transform(state)


def inversion_0_unitary(U, s):
    n = int(log2(len(s)))
    assert (U.shape[0] == 2 ** n)
    assert (U.shape[1] == 2 ** n)

    state = dagger(U) @ s

    # assert is_close(state[0].imag, 0) # only in Grover context

    # state[0] = state[0] - 2*state[0].conjugate()
    # for k in range(len(state)):
    #     state[k] = -state[k]

    inversion(init_state(n), state)

    state = U @ state

    for k in range(len(s)):
        s[k] = state[k]


def grover_sim_unitary(U, predicate, iterations):
    assert (U.shape[0] == U.shape[1])
    n = int(log2(U.shape[0]))

    state = U @ init_state(n)

    # Grover iterate
    for _ in range(iterations):
        # oracle (reflection in bad state vector)
        oracle(state, predicate)

        # inversion (reflection in original state)
        # inversion(s, state)
        # inversion_direct(s, state)
        inversion_0_unitary(U, state)

    return state


# n = number of qubits,
# l = number of items
# j = iteration number
def target_amplitude_uniform(n, l, j):
    theta = asin(sqrt(l / 2 ** n))
    return sin((2 * j + 1) * theta) / sqrt(l)  # (-1)**j* without - in iterate
    # return sin((2*j+1)*asin(sqrt(l/2**n)))/sqrt(l)


# n = number of qubits,
# it = iteration number
# k = outcome
# phi = angle of ry rotations
def target_amplitude_binomial(n, it, k, phi):
    m = bin(k).count("1")
    theta = asin(sin(phi / 2) ** m * cos(phi / 2) ** (n - m))
    return sin((2 * it + 1) * theta)


def grover_circuit(A, O, iterations):
    n = A.num_qubits
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(A, q)

    for i in range(1, iterations + 1):
        qc.append(grover_iterate_circuit(A, O), q)

    return qc


def is_bit_not_set(m, k):
    return not (m & (1 << k))


def phase_oracle_match(n, items):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for m in items:
        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])

        qc.mcp(pi, [q[i] for i in range(len(q) - 1)], q[len(q) - 1])

        for i in range(n):
            if is_bit_not_set(m, i):
                qc.x(q[i])
    return qc


def inversion_circuit(prepare):
    n = prepare.num_qubits
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    qc.append(prepare.inverse(), q)

    # for i in range(n):
    #     qc.x(q[i])
    #
    # # controlled Z
    # qc.mcp(pi, [q[i] for i in range(n - 1)], q[n - 1])
    #
    # for i in range(n):
    #     qc.x(q[i])
    qc.append(inversion_0_circuit(n), q)

    qc.append(prepare, q)

    return qc


def inversion_0_circuit(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(n):
        qc.x(q[i])

    # controlled Z
    qc.mcp(pi, [q[i] for i in range(n - 1)], q[n - 1])

    for i in range(n):
        qc.x(q[i])

    return qc


def grover_iterate_circuit(prepare, oracle):
    n = oracle.num_qubits
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    # oracle
    qc.append(oracle, q)

    # inversion by the mean
    qc.append(inversion_circuit(prepare), q)

    return qc


def amplitude_estimation_circuit(n, prepare, oracle, swap=True):
    c = QuantumRegister(n)
    q = QuantumRegister(prepare.num_qubits)
    qc = QuantumCircuit(c, q)

    qc.append(prepare, q)
    # qc.report('A')

    for i in range(n):
        qc.h(c[i])

    for i in range(n):
        for _ in range(2 ** i):
            if swap:
                qc.c_append(grover_iterate_circuit(prepare, oracle), c[i], q)
            else:
                qc.c_append(grover_iterate_circuit(prepare, oracle), c[n - 1 - i], q)

    qc.iqft(c if swap else c[::-1], swap)
    # qc.append_iqft(c, not swap, swap)

    return qc


def simple_amplitude_estimation_circuit(prepare, oracle, iterations):
    c = QuantumRegister(1)
    q = QuantumRegister(prepare.num_qubits)
    qc = QuantumCircuit(c, q)

    qc.append(prepare, q)
    # qc.report('A')

    qc.h(c[0])

    for _ in range(iterations):
        qc.c_append(grover_iterate_circuit(prepare, oracle), c[0], q)

    qc.h(c[0])

    return qc


def list_to_dict(state, show_binary=True):
    n = int(log2(len(state)))
    return dict(zip([str(k) + (('=' + padded_bin(n, k)) if show_binary else '') for k in range(len(state))],
                    [state[k] for k in range(len(state))]))


def prepare_uniform(n):
    q = QuantumRegister(n)
    qc = QuantumCircuit(q)

    for i in range(len(q)):
        qc.h(q[i])

    return qc
