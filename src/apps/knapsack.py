from math import ceil, log2

from hume import QuantumRegister, QuantumCircuit
from apps.utils import knapsack_table_new
from hume.algos.grover_optimizer import grover_optimizer, oracle_match_0_multi
from hume.algos.function_encoding import encode_term
from hume.utils.common import padded_bin


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

    circuit.iqft(value[::-1], swap=False)

    # encode weight function
    for (coeff, vars) in w:
        encode_term(coeff, vars, circuit, key, weight)

    circuit.iqft(weight[::-1], swap=False)

    return circuit


def terms(l):
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


def solve_knapsack(values, weights, max_weight):

    def action_on_progress(flow_state):
        n_key = flow_state['circuit_params']['n_key']
        n_value = flow_state['circuit_params']['n_value']
        n_weight = flow_state['circuit_params']['n_weight']
        s = flow_state['last_run_result']['state vector']
        print(knapsack_table_new(s, n_key, n_value, n_weight))

        print(f'\nLooking for values >= {flow_state["circuit_params"]["min_value"]}')


    assert(len(values) == len(weights))
    n_key = len(values)

    v = terms(values)
    w = terms(weights)

    v_adjusted = [(-max(values) - 0, [])] + v
    w_adjusted = [(-item[0], item[1]) for item in w] + [(max_weight, [])]

    min_value = max(values)
    n_value = ceil(log2(max(min_value, sum(values) - min_value))) + 1

    # weight register size based on w_adjusted
    n_weight = ceil(log2(sum([max_weight - item[0] for item in w]))) + 1

    oracle = oracle_match_0_multi(n_key + n_value + n_weight,
                                  [n_key + n_value - 1, n_key + n_value + n_weight - 1])

    def process_outcome(outcome, flow_state):
        n = flow_state['circuit_params']['n_key'] + flow_state['circuit_params']['n_value'] + flow_state['circuit_params']['n_weight']
        outcome_selection = padded_bin(n, outcome)[-n_key:]
        outcome_value = get_selection_value(outcome_selection, v)
        outcome_weight = get_selection_weight(outcome_selection, w)
        return outcome_selection, outcome_value, outcome_weight

    def update_circuit_params(outcome_results, flow_state):
        circuit_params = flow_state['circuit_params']
        outcome_selection, outcome_value, outcome_weight = outcome_results
        v = circuit_params['v']

        # adjust value function
        # v_adjusted = v + [(-outcome_value - 0, [])]
        v[0] = (-outcome_value - 1, [])

        # circuit_params['v'] = v_adjusted

        circuit_params['min_value'] = outcome_value + 1
        action_on_progress(flow_state)

    def progress(results, flow_state):
        outcome_selection, outcome_value, outcome_weight = results
        min_value = flow_state['circuit_params']['min_value']
        return (outcome_value >= min_value) and (outcome_weight <= max_weight)

    def build_circuit(flow_state):
        return build_knapsack_circuit(flow_state['circuit_params']['n_key'], flow_state['circuit_params']['n_value'], flow_state['circuit_params']['n_weight'],
                                      flow_state['circuit_params']['v'], flow_state['circuit_params']['w'])

    results = grover_optimizer({'n_key': n_key, 'n_value': n_value, 'n_weight': n_weight, 'v': v_adjusted, 'w': w_adjusted, 'min_value': min_value},
                     build_circuit, oracle,
                     update_circuit_params, progress, process_outcome, failure_threshold=3)

    items_string = results[0]
    items = [str(len(items_string) - 1 - k) for k in range(len(items_string)) if items_string[k] == '1'][::-1]

    print(f'Optimal selection consists of items {", ".join(items)}. The combined value is {results[1]}, and the '
          f'combined weight is {results[2]}.')


def test_knapsack():
    values = [2, 3, 1]
    weights = [3, 2, 1]
    max_weight = 4


    solve_knapsack(values, weights, max_weight)