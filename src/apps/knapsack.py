import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

from math import ceil, log2, pi, floor, log10, atan2
from sty import bg, Style, RgbBg, fg

from hume.algos.grover import grover_circuit
from hume.simulator.circuit import QuantumRegister, QuantumCircuit
from hume.utils.common import padded_bin, complex_to_rgb

# CONFIG.use_mpl(True)


def encode_term(coeff, vars, circuit, key, value):
    for i in range(len(value)):
        if len(vars) > 1:
            circuit.mcp(pi * 2 ** -i * coeff, [key[j] for j in vars], value[i])
        elif len(vars) > 0:
            circuit.cp(pi * 2 ** -i * coeff, key[vars[0]], value[i])
        else:
            circuit.p(pi * 2 ** -i * coeff, value[i])


def build_knapsack_circuit(n_key, n_value, n_weight, v, w):
    key = QuantumRegister(n_key)
    value = QuantumRegister(n_value)
    weight = QuantumRegister(n_weight)
    circuit = QuantumCircuit(key, value, weight)

    for i in range(len(key)):
        circuit.h(key[i])

    for i in range(len(value)):
        circuit.h(value[i])

    for i in range(len(weight)):
        circuit.h(weight[i])

    # encode value function
    for (coeff, vars) in v:
        encode_term(coeff, vars, circuit, key, value)

    # circuit.iqft(value[::-1], swap=False)
    circuit.append_iqft(value, reversed=True, swap=False)

    # encode weight function
    for (coeff, vars) in w:
        encode_term(coeff, vars, circuit, key, weight)

    # circuit.iqft(weight[::-1], swap=False)
    circuit.append_iqft(weight, reversed=True, swap=False)

    return circuit


def oracle_match_0_multi(bits, tag_bits):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    for t in tag_bits:
        qc.x(q[t])

    qc.mcp(pi, [q[t] for t in tag_bits[:-1]], q[len(q) - 1])

    for t in tag_bits:
        qc.x(q[t])

    return qc


def coeffs(l):
    return  [(l[k], [k]) for k in range(len(l))]


def get_selection_value(selection_binary, v):
    val = 0
    for i in range(len(selection_binary)):
        val += int(selection_binary[::-1][i]) * v[i][0]

    return val


def get_selection_weight(selection_binary, w):
    weight = 0
    for i in range(len(selection_binary)):
        weight += int(selection_binary[::-1][i]) * w[i][0]

    return weight


def solve_knapsack_with_min_value(values, weights, max_weight, min_value=0, visualize_steps=False):
    # key register (qubit for each item in the problem)
    assert(len(values) == len(weights))
    n_key = len(values)

    v = coeffs(values)
    w = coeffs(weights)

    # weight register size based on w_adjusted
    n_weight = ceil(log2(sum([max_weight - item[0] for item in w]))) + 1

    progress = True
    while progress:
        r = find_selection_with_min_value(min_value, max_weight, n_key, n_weight, v, visualize_steps, w)
        yield(r)
        if r[0] is None:
            progress = False
        else:
            min_value = r[1] + 1


def solve_knapsack(values, weights, max_weight, visualize_steps=False):
    # start with highest value as highest single item value and max_weight
    highest_item_value = max(values)

    return solve_knapsack_with_min_value(values, weights, max_weight, min_value=highest_item_value, visualize_steps=visualize_steps)


def find_selection_with_min_value(min_value, max_weight, n_key, n_weight, v, visualize_steps, w):
    # adjust weight function and add max weight term
    w_adjusted = [(-item[0], item[1]) for item in w] + [(max_weight, [])]

    # adjust value function
    v_adjusted = v + [(-min_value, [])]

    # value register size based on max value
    n_value = ceil(log2(max(min_value, sum([item[0] for item in v]) - min_value))) + 1

    n = n_key + n_value + n_weight

    prepare = build_knapsack_circuit(n_key, n_value, n_weight, v_adjusted, w_adjusted)
    oracle = oracle_match_0_multi(n_key + n_value + n_weight, [n_key + n_value - 1, n_key + n_value + n_weight - 1])

    solution_selection = None
    solution_value = None

    qc = grover_circuit(prepare, oracle, 1)

    result = qc.measure(shots=100)

    outcome = max(result['counts'].items(), key=lambda k: k[1])[0]
    outcome_selection = padded_bin(n, outcome)[-n_key:]
    outcome_value = get_selection_value(outcome_selection, v)

    if visualize_steps:
        print("\nChecking min value:", min_value)
        print(knapsack_table_new(result['state vector'], n_key, n_value, n_weight))
        # grid_state(result['state vector'], m=n_key, neg=True, show_probs=False)

    if outcome_value >= min_value:
        # check that it is a valid solution
        outcome_weight = get_selection_weight(outcome_selection, w)
        if outcome_weight <= max_weight :
            solution_value = outcome_value
            solution_selection = outcome_selection
            if visualize_steps:
                print(f"\nFound selection {solution_selection} with value {solution_value}")

    return solution_selection, solution_value, qc.run()


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


def poly(n_key, coeffs):
    p = [0 for _ in range(2**n_key)]
    for k in range(2**n_key):
        b = padded_bin(n_key, k)
        # print(b)
        p_k = 0
        for m in coeffs:
            p_k_m = m[0]
            for idx in m[1]:
                p_k_m *= int(b[n_key-1-idx])
            p_k += p_k_m
        # print(k, '=', b, '-->', p_k)
        p[k] = p_k

    return p


def find_optimal_selection(item_values, item_weights, max_weight, visualize_steps=True, min_value=None, action=None):

    if min_value is None:
        min_value = max(item_values)

    knapsack_solutions = solve_knapsack_with_min_value(item_values, item_weights, max_weight, min_value, visualize_steps)
    best = None
    for solution in knapsack_solutions:
        if solution[0] is not None:
            best = solution[0]
            # print_state_table(solution[2])

            if action is not None:
                n_key = len(item_values)
                n_value = ceil(log2(max(min_value, sum(item_values) - min_value))) + 1
                n_weight = ceil(log2(sum([max_weight - item for item in item_weights]))) + 1

                action(solution[2], n_key, n_value, n_weight)

    items = [str(len(best) - 1 - k) for k in range(len(best)) if best[k] == '1'][::-1]
    p_v = poly(len(best), coeffs(item_values))
    p_w = poly(len(best), coeffs(item_weights))
    idx = int(best, 2)

    return (f'Optimal selection consists of items {", ".join(items)}. The combined weight is {p_w[idx]}, and the '
            f' combined value is {p_v[idx]}.')


if __name__ == "__main__":
# def test():
    values = [2, 3, 1]
    weights = [3, 2, 1]
    max_weight = 4

    action = lambda state,  n_key, n_value, n_weight: print(knapsack_table_new(state, n_key, n_value, n_weight))
    print('\n', find_optimal_selection(values, weights, max_weight, False, None, action))
