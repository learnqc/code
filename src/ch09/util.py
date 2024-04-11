from ch08.util import *
from math import log2
import matplotlib.pyplot as plt
from sty import fg


def padded_bin(n, k):
    return bin(k)[2:].zfill(n)


def rev(n, k):
    return int(bin(k)[2:].zfill(n)[::-1], 2)


def reverse_index_state(state):
    n = int(log2(len(state)))
    s = state.copy()
    for k in range(len(state)):
        s[k] = state[int(padded_bin(n, k)[::-1], 2)]
    return s


def list_to_dict(state, show_binary=True):
    n = int(log2(len(state)))
    return dict(zip([str(k) + (('=' + padded_bin(n, k)) if show_binary else '') for k in range(len(state))],
                    [state[k] for k in range(len(state))]))


def plot_bars(bars, title, title_x, title_y, color=None, fig_name=None, action=lambda plt: None):
    if isinstance(bars, list):
        bars = dict(zip(range(len(bars)), bars))
    _, ax = plt.subplots()

    y_position = range(len(bars))
    ax.bar(y_position, [abs(v) for v in bars.values()], align='center',  # width=0.257,
           color=color if color is not None else [[x for x in complex_to_rgb(round(v, 5))] for v in bars.values()])
    plt.xticks(y_position, bars.keys())
    if len(bars) > 16:
        plt.xticks(rotation=90, fontsize=10)
    else:
        plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title)
    plt.tight_layout()
    fig = plt.gcf()
    action(ax)
    plt.show()
    if fig_name:
        fig.savefig(fig_name)


def dagger(U):
    return U.T.conj()
