from math import log2, ceil, floor
from random import choices
from collections import Counter

from hume.utils.common import is_close


def is_power_of_two(m):
    return ceil(log2(m)) == floor(log2(m))


def prepare_state(*a):
    state = [a[k] for k in range(len(a))]
    assert (is_power_of_two(len(state)))
    assert (is_close(sum([abs(state[k]) ** 2 for k in range(len(state))]), 1.0))
    return state


def init_state(n):
    state = [0 for _ in range(2 ** n)]
    state[0] = 1
    return state


def is_bit_set(m, k):
    return m & (1 << k) != 0


def pair_generator_check_digit(n, t):
    distance = int(2 ** t)

    for k0 in range(2 ** n):
        if not is_bit_set(k0, t):
            k1 = k0 + distance
            yield k0, k1


def pair_generator_concatenate(n, t):
    distance = int(2 ** t)
    suffix_count = int(2 ** t)
    prefix_count = int(2 ** (n - t - 1))

    for p in range(prefix_count):
        for s in range(suffix_count):
            k0 = p * suffix_count * 2 + s
            k1 = k0 + distance
            yield k0, k1


def pair_generator_pattern(n, t):
    distance = int(2 ** t)

    for j in range(2 ** (n - t - 1)):
        for k0 in range(2 * j * distance, (2 * j + 1) * distance):
            k1 = k0 + distance
            yield k0, k1


pair_generator = pair_generator_concatenate


def process_pair(state, gate, k0, k1):
    x = state[k0]
    y = state[k1]
    # new amplitudes
    state[k0] = x * gate[0][0] + y * gate[0][1]
    state[k1] = x * gate[1][0] + y * gate[1][1]


def transform(state, t, gate):
    n = int(log2(len(state)))
    for (k0, k1) in pair_generator(n, t):
        process_pair(state, gate, k0, k1)


def c_transform(state, c, t, gate):
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: is_bit_set(p[0], c), pair_generator(n, t)):
        process_pair(state, gate, k0, k1)


def mc_transform(state, cs, t, gate):
    assert t not in cs
    n = int(log2(len(state)))
    for (k0, k1) in filter(lambda p: all([is_bit_set(p[0], c) for c in cs]), pair_generator(n, t)):
        process_pair(state, gate, k0, k1)


def measure(state, shots):
    samples = choices(range(len(state)), [abs(state[k]) ** 2 for k in range(len(state))], k=shots)
    counts = {}
    for (k, v) in Counter(samples).items():
        counts[k] = v
    return counts


def transform_u(state, U, t):
    assert (U.shape[0] == U.shape[1])
    m = int(log2(U.shape[0]))
    n = int(log2(len(state)))

    vec = [_ for _ in range(2 ** m)]

    for suffix in range(2 ** t):
        for prefix in range(2 ** (n - m - t)):
            for target in range(2 ** m):
                k = prefix * 2 ** (t + m) + target * 2 ** t + suffix
                vec[target] = state[k]

            vec_out = U @ vec

            for target in range(2 ** m):
                k = prefix * 2 ** (t + m) + target * 2 ** t + suffix
                state[k] = vec_out[target]


def c_transform_u(state, U, c, t):
    assert (U.shape[0] == U.shape[1])
    m = int(log2(U.shape[0]))
    n = int(log2(len(state)))

    vec = [_ for _ in range(2 ** m)]

    for suffix in range(2 ** t):
        for prefix in range(2 ** (n - m - t)):
            targets = []
            for idx in range(2 ** m):
                k = prefix * 2 ** (t + m) + idx * 2 ** t + suffix
                if k & (1 << c):
                    # if is_bit_set(k, c):
                    vec[idx] = state[k]
                    targets.append(k)

            vec_out = U @ vec

            for idx in range(2 ** m):
                k = prefix * 2 ** (t + m) + idx * 2 ** t + suffix
                # if k & (1 << c):
                if is_bit_set(k, c):
                    state[k] = vec_out[idx]
