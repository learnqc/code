from math import cos, sin, pi, atan2, log2, floor, log10

from sty import fg

from ch03.scalar_map import scalarMap


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
    return cos(theta) + 1j*sin(theta)


def complex_to_rgb(c, ints=False):
    a = c.real
    b = c.imag

    hue = atan2(b, a)/pi*180
    if hue < 0:
        hue += 360

    rgb = scalarMap.to_rgba(hue)[:3]

    if ints:
        r, g, b = tuple([int(round(c * 255.0)) for c in rgb])
        return r, g, b
    else:
        return rgb


def print_state_table(state, decimals=4, symbol='\u2588'):
    print(state_table_to_string(state, decimals, symbol))


def state_table_to_string(state, decimals=4, symbol='\u2588'):
    assert(decimals <= 10)
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j * round(state[k].imag, decimals) for k in range(len(state))]

    headers = ['Outcome', 'Binary', 'Amplitude', 'Magnitude', 'Direction', 'Amplitude Bar', 'Probability']
    offsets = [max(len(headers[0]), floor(log10(len(state)))),               # outcome
               max(len(headers[1]), n),                                      # binary
               max(len(headers[2]), 2*(decimals + 2) + 6),                   # amplitude
               max(len(headers[3]), (decimals + 2)),                         # magnitude
               max(len(headers[4]), decimals),                               # direction
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

                             str(round(abs(state[k]), decimals)).ljust(decimals + 2, ' ').ljust(offsets[3], ' '),

                             (str(((' ' if direction >= 0 else '-') + str(floor(abs(direction)))).rjust(4, ' ') +
                                  '.' + str(int(100*round(direction - floor(direction), 2))).ljust(2, '0')) + '\u00b0' if
                              abs(round_state[k]) > 0 else offsets[4] * ' ').ljust(offsets[4], ' '),

                             fg(*[int(255*a) for a in complex_to_rgb(state[k])]) + (int(abs(state[k] * 24)) * symbol).ljust(offsets[5], ' ') + fg.rs,

                             str(round(abs(state[k]) ** 2, decimals)).ljust(decimals + 2, ' ')
                             ])
        output += '\n'

    return output
