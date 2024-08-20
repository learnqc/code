from math import floor, log10, atan2, log2, pi

from sty import RgbBg, Style, bg, fg

from hume.utils.common import padded_bin
from hume.utils.common import complex_to_rgb


def knapsack_table_new(state, key_size, value_size, weight_size, decimals=4, symbol='\u2588', colors=None):
    n = int(log2(len(state)))
    round_state = [round(state[k].real, decimals) + 1j * round(state[k].imag, decimals) for k in range(len(state))]

    headers = ['Selection', 'Value', 'Binary', 'Weight', 'Binary', 'Magnitude', 'Direction', 'Amplitude Bar']
    offsets = [
        # max(len(headers[0]), floor(log10(len(state)))),  # outcome key
        max(len(headers[0]), key_size),                  # binary key
        max(len(headers[1]), floor(log10(len(state)))),  # outcome value
        max(len(headers[2]), value_size),                # binary value
        max(len(headers[3]), floor(log10(len(state)))),  # outcome weight
        max(len(headers[4]), n-key_size-value_size),                # binary weight
        # max(len(headers[4]), 2 * (decimals + 2) + 6),  # amplitude
        max(len(headers[5]), (decimals + 2)),            # magnitude
        max(len(headers[6]), decimals),                  # direction
        max(len(headers[7]), 24),                        # amplitude bar
        # max(len(headers[8]), decimals + 2),              # probability
    ]

    for i in range(len(offsets)):
        headers[i] = headers[i] + ' ' * (offsets[i] - len(headers[i]))

    header_str = '  '.join(headers)

    output = '\n'
    # output += '\033[1m' + '      Key             Value' + '\033[0m'
    # output += '\n'
    output += header_str
    output += '\n'
    output += len(header_str) * '-'
    output += '\n'

    ind_to_color = []  # array containing the color for each row index

    # populate ind_to_color with None for each row
    for i in range(len(round_state)):
        ind_to_color.append(None)

    # add the color for each index that's supposed to be colored
    if colors is not None:
        for key in colors:
            for index in colors.get(key):
                assert(not ind_to_color[index]) # make sure each index is only assigned one color
                ind_to_color[index] = key

    rows = []
    for k in range(len(round_state)):
        if abs(round_state[k]) > 0.0001:
            direction = round(atan2(round_state[k].imag, round_state[k].real) * 180 / pi, 2)

            # if we're creating a row that has a background color specified, get the color
            if ind_to_color[k]:
                bg.my_color = Style(RgbBg(ind_to_color[k][0], ind_to_color[k][1], ind_to_color[k][2]))

            rows += [[
                # str(int(padded_bin(n, k)[-key_size:], 2)).ljust(offsets[0], ' '),

                padded_bin(n, k)[-key_size:].ljust(offsets[0], ' '),

                str(int(padded_bin(n, k)[weight_size:-key_size], 2)).ljust(offsets[1], ' '),

                padded_bin(n, k)[weight_size:-key_size].ljust(offsets[2], ' '),

                str(int(padded_bin(n, k)[0:weight_size], 2)).ljust(offsets[3], ' '),

                padded_bin(n, k)[0:weight_size].ljust(offsets[4], ' '),

                str(round(abs(state[k]), decimals)).ljust(decimals + 2, ' ').ljust(offsets[5], ' '),

                (str(((' ' if direction >= 0 else '-') + str(floor(abs(direction)))).rjust(4, ' ') +
                     '.' + str(int(100 * round(direction - floor(direction), 2))).ljust(2, '0')) + '\u00b0' if
                 abs(round_state[k]) > 0 else offsets[6] * ' ').ljust(offsets[6], ' '),

                fg(*[int(255 * a) for a in complex_to_rgb(state[k])]) + (
                        int(abs(state[k] * 24)) * symbol).ljust(offsets[7], ' ') + fg.rs

                # str(round(abs(state[k]) ** 2, decimals)).ljust(decimals + 2, ' ') + bg.rs
            ]]

    sorted_rows = sorted(rows, key=lambda x: int(x[0]))

    for row in sorted_rows:
        output += '  '.join(row)
        output += '\n'

    return output

