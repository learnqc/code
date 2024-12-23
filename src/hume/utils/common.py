import random
from math import cos, sin, pi, log2, log10, atan2, floor, sqrt
from sty import fg

from hume.utils.scalar_map import plt, plt, scalarMap


def is_close_float(a, b, rtol=1e-5, atol=1e-8):
    return abs(a - b) < atol + rtol * abs(b)


def is_close(a, b):
    if isinstance(a, float):
        a = complex(a, 0)

    if isinstance(b, float):
        b = complex(b, 0)

    return is_close_float(a.real, b.real) and is_close_float(a.imag, b.imag)


def all_close(state1, state2):
    for (a, b) in zip(state1, state2):
        if not is_close(a, b):
            return False
    return True


def cis(theta):
    return cos(theta) + 1j * sin(theta)


# class Config:
#     def __init__(self, mpl=True):
#         self.use_mpl(mpl)
#
#     def use_mpl(self, mpl=True):
#         self.mpl = mpl
#         if self.mpl:
#             self.scalarMap = scalarMap
#
#     def get_use_mpl(self):
#         return self.mpl


# CONFIG = Config()


def show_state_table(state, decimals=4):
    print_state_table(state, decimals)


def complex_to_rgb(c, ints=False):
    a = c.real
    b = c.imag

    hue = atan2(b, a) / pi * 180
    if hue < 0:
        hue += 360

    rgb = scalarMap.to_rgba(hue)[:3]

    if ints:
        return [int(round(c * 255.0)) for c in rgb]
    else:
        return rgb


def to_table(s, decimals=4):
    n = int(log2(len(s)))

    round_state = [round(s[k].real, decimals) + 1j * round(s[k].imag, decimals) for k in range(len(s))]
    table = [[k, bin(k)[2:].zfill(n),
              ('+' if round_state[k].real >= 0 else '-') + str(abs(round_state[k].real)).ljust(decimals + 2, '0') +
              (' + ' if round_state[k].imag >= 0 else ' - ') + str(abs(round_state[k].imag)).ljust(decimals + 2,
                                                                                                   '0') + '*i',
              abs(s[k]),
              str(0 if s[k] == 0.0 else round(atan2(s[k].imag, s[k].real) / (2 * pi) * 360, 2)) + '\u00b0',
              int(floor(24 * abs(s[k]))) * '\u2588',
              abs(s[k]) ** 2] for k in range(len(s))]
    table_r = [[round(x, decimals) if isinstance(x, float) else round(x.real, decimals) + 1j * round(x.imag,
                                                                                                     decimals) if isinstance(
        x, complex) else x for x in table[k]] for k in range(len(table))]
    return table_r


def state_table_to_string(state, decimals=4, symbol='\u2588'):
    assert(decimals <= 10)
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j * round(state[k].imag, decimals) for k in range(len(state))]

    headers = ['Outcome', 'Binary', 'Amplitude', 'Direction', 'Magnitude', 'Amplitude Bar', 'Probability']
    offsets = [max(len(headers[0]), floor(log10(len(state)))),               # outcome
               max(len(headers[1]), n),                                      # binary
               max(len(headers[2]), 2*(decimals + 2) + 6),                   # amplitude
               max(len(headers[4]), decimals),                               # direction
               max(len(headers[3]), (decimals + 2)),                         # magnitude
               max(len(headers[5]), 24),                                     # amplitude bar
               max(len(headers[6]), decimals + 2),                           # probability
               ]

    for i in range(len(offsets)):
        headers[i] = headers[i] + ' '*(offsets[i] - len(headers[i]))

    header_str = '  '.join(headers)

    output = '\n' + header_str + '\n' + len(header_str) * '-' + '\n'

    for k in range(len(round_state)):
        direction = round(atan2(round_state[k].imag, round_state[k].real) * 180 / pi, 2)

        output += '  '.join([str(k).ljust(offsets[0], ' '),

                             str(bin(k)[2:].zfill(n)).ljust(offsets[1] - 1, ' '),

                             ((' ' if round_state[k].real >= 0 else '-') +
                              str(abs(round_state[k].real)).ljust(decimals + 2, '0') +
                              (' + ' if round_state[k].imag >= 0 else ' - ') + 'i' +
                              str(abs(round_state[k].imag)).ljust(decimals + 2, '0')).ljust(offsets[2] + 1, ' '),

                             (str(((' ' if direction >= 0 else '-') + str(floor(abs(direction)))).rjust(4, ' ') +
                                  '.' + str(int(100*round(abs(direction) - floor(abs(direction)), 2))).ljust(2, '0')) + '\u00b0' if
                              abs(round_state[k]) > 0 else offsets[4] * ' ').ljust(offsets[4], ' '),

                             str(round(abs(state[k]), decimals)).ljust(decimals + 2, ' ').ljust(offsets[3], ' '),

                             fg(*[int(255*a) for a in complex_to_rgb(state[k])]) + (int(abs(state[k] * 24)) * symbol).ljust(offsets[5], ' ') + fg.rs,

                             str(round(abs(state[k]) ** 2, decimals)).ljust(decimals + 2, ' ')
                             ])
        output += '\n'

    return output


def print_state_table(state, decimals=4, symbol='\u2588'):
    print(state_table_to_string(state, decimals, symbol))


def prod(iterable):
    p = 1
    for n in iterable:
        p *= n
    return p


def rev(n, k):
    return int(bin(k)[2:].zfill(n)[::-1], 2)


def padded_bin(n, k):
    return bin(k)[2:].zfill(n)


def reverse_index_state(state):
    n = int(log2(len(state)))
    s = state.copy()
    for k in range(len(state)):
        s[k] = state[int(padded_bin(n, k)[::-1], 2)]
    return s


def inner(v1, v2):
    assert (len(v1) == len(v2))
    return sum(z1 * z2.conjugate() for z1, z2 in zip(v1, v2))


def list_to_dict(state, show_binary=True):
    n = int(log2(len(state)))
    return dict(zip([str(k) + (('=' + padded_bin(n, k)) if show_binary else '') for k in range(len(state))],
                    [state[k] for k in range(len(state))]))


def generate_state(n, seed=555):
    # Choose a seed
    random.seed(seed)
    # Generate random probabilities that add up to 1
    probs = [random.random() for _ in range(2**n)]
    total = sum(probs)
    probs = [p / total for p in probs]
    # Generate random angles in radians
    angles = [random.uniform(0, 2 * pi) for _ in range(2**n)]
    # Build the quantum state array
    return [sqrt(p) * (cos(a) + 1j * sin(a)) for (p, a) in zip(probs, angles)]
