from sty import bg

from ch09.util import *


def complex_to_rgb_ints(c):
    return [int(round(c * 255.0)) for c in complex_to_rgb(c)]


def grid_state_horiz(state, m=0, neg=False, show_probs=False):
    n = int(log2(len(state)))
    cols = 2**m
    rows = int(len(state) / cols) # first register
    from tabulate import tabulate
    print('\n')
    if neg:
        print(tabulate([[str(k) + ' = ' + bin(k)[2:].zfill(n-m)] + [
            bg(*complex_to_rgb_ints(state[l*rows + k]))+ int(abs(state[l*rows + k] * 10)) * ' ' + bg.rs +
            (' ' + (str(round(abs(state[l*rows + k])**2, 2)) if abs(state[l*rows + k]) > 0.01 else '') if show_probs else '')
            for l in list(range(int(cols/2), cols)) + list(range(int(cols/2)))] for k in range(rows)],
                       headers=[(str(l) if l < cols/2 else str(l - cols)) + ' = ' + bin(l)[2:].zfill(m)
                                for l in list(range(int(cols/2), cols)) + list(range(int(cols/2)))],
                       tablefmt='fancy_grid'))
    else:
        print(tabulate([[str(k) + ' = ' + bin(k)[2:].zfill(n-m)] + [
            bg(*complex_to_rgb_ints(state[l*rows + k]))+ int(abs(state[l*rows + k] * 10)) * ' ' + bg.rs +
            (' ' + (str(round(abs(state[l*rows + k])**2, 2)) if abs(state[l*rows + k]) > 0.01 else '') if show_probs else '')
            for l in range(cols)] for k in range(rows)],
                       headers=[str(l) + ' = ' + bin(l)[2:].zfill(m) for l in range(cols)],
                       tablefmt='fancy_grid'))


def grid_state(state, m=1, neg=False, show_probs=False):
    n = int(log2(len(state))) - m
    cols = 2**m
    rows = int(len(state) / cols) # first register
    from tabulate import tabulate
    print('\n')
    if neg:
        print(tabulate([[(str(k) if k < rows/2 else str(k - rows)) + ' = ' + bin(k)[2:].zfill(n)] + [
            bg(*complex_to_rgb_ints(state[k*cols + l]))+ int(abs(state[k*cols + l] * 10)) * ' ' + bg.rs +
            (' ' + (str(round(abs(state[k*cols + l])**2, 2)) if abs(state[k*cols + l]) > 0.01 else '') if show_probs else '')
            for l in range(cols)] for k in list(range(int(rows/2)))[::-1] + list(range(int(rows/2), rows))[::-1]],
                       headers=[str(l) + ' = ' + bin(l)[2:].zfill(m) for l in range(cols)],
                       tablefmt='fancy_grid'))
    else:
        print(tabulate([[str(k) + ' = ' + bin(k)[2:].zfill(n)] + [
            bg(*complex_to_rgb_ints(state[k*cols + l]))+ int(abs(state[k*cols + l] * 10)) * ' ' + bg.rs +
            (' ' + (str(round(abs(state[k*cols + l])**2, 2)) if abs(state[k*cols + l]) > 0.01 else '') if show_probs else '')
            for l in range(cols)] for k in range(rows)[::-1]],
                       headers=[str(l) + ' = ' + bin(l)[2:].zfill(m) for l in range(cols)],
                       tablefmt='fancy_grid'))