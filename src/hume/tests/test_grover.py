from math import asin, sqrt, pi, sin

import hume.qiskit
from build.lib.hume.utils.common import print_state_table
from hume.algos.grover import grover_sim, grover_sim_unitary, oracle, inversion, \
    inversion_0_transformation, amplitude_estimation_circuit, phase_oracle_match, prepare_uniform
from hume.simulator.core import init_state
from hume.tests.test_unitary import complex_sincd
from hume.utils.common import all_close, is_close
from hume.utils.matrix import as_array, argmax, rvs, random_transformation


def test_grover_sims():
    n = 3

    items = [3, 5]
    predicate = lambda i: True if i in items else False

    U = rvs(2 ** n)

    s = U[:, 0]  # state prepared by U

    iterations = 1

    state1 = s.tolist()
    grover_sim(state1, predicate, iterations)
    print('\n', as_array(state1))

    state2 = grover_sim_unitary(U, predicate, iterations)
    print('\n', state2)

    assert all_close(state1, state2)


def test_inversions_transformation():
    n = 3

    predicate = lambda k: True if k == 3 else False

    f = random_transformation(n)
    original_state = init_state(n)
    f[0](original_state)

    state1 = original_state.copy()
    oracle(state1, predicate)
    inversion(original_state.copy(), state1)
    print('\n', state1)

    state2 = original_state.copy()
    oracle(state2, predicate)
    inversion_0_transformation(f, state2)
    print('\n', state2)

    assert all_close(state1, state2)


def test_amplitude_estimation():
    n = 4
    m = 3

    for l in range(2 ** m):
        items = list(range(l))
        print('\nitems = ', list(items))
        qc = amplitude_estimation_circuit(n, prepare_uniform(m), phase_oracle_match(m, items), False)
        state = qc.run()

        # print_state_table(state)

        probs = [0 for _ in range(2 ** n)]

        for j in range(2 ** n):  # suffix
            for k in range(2 ** m):  # prefix
                probs[j] += abs(state[k * 2 ** n + j]) ** 2

        # from count to v
        # theta = 2 * asin(sqrt(len(items) / 2 ** m))
        # v = theta / 2 / pi * 2 ** n
        v = 2 ** n / pi * asin(sqrt(len(items) / 2 ** m))

        # sincd = [abs(a) ** 2 for a in complex_sincd(n - 1, v)]

        for k in range(1, len(probs) // 2):
            assert is_close(abs(probs[k]) ** 2, abs(probs[len(probs) - k]) ** 2)

        probs1 = [probs[0] + probs[len(probs) // 2]] + [probs[k - len(probs) // 2] + probs[k + len(probs) // 2] for k in
                                                        range(1, len(probs) // 2)]

        assert all(abs(probs1[k] - abs(complex_sincd(n - 1, v)[k]) ** 2) < 0.01 for k in range(0, len(probs1)))

        sines = {}
        for k, v in enumerate(probs[int(len(probs) / 2):]):
            key = 2 ** m * round(sin(k * pi / 2 ** n) ** 2, 4)
            sines[key] = sines.get(key, 0) + round(v, 4)

        count = round(max(sines, key=sines.get))
        print('count ~ ', count)

        v = argmax(probs[int(len(probs) / 2):])
        count1 = int(2 ** m * sin(v * pi / 2 ** n) ** 2)
        print('count1 ~ ', count1)
