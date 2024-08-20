from hume.algos.grover_optimizer import oracle_match_0, grover_optimizer
from hume.algos.function_encoding import build_polynomial_circuit, poly
from hume.utils.common import padded_bin


def test_grover_optimizer():
    n_key = 3
    n_value = 6

    terms = ([(-6, [])] + [(6*2**k, [k]) for k in range(n_key)] +
             [(-2**(j+k), ([j, k] if j != k else [j]))  for j in range(n_key) for k in range(n_key)]) # squares

    p = poly(n_key, terms, False)
    f = lambda k: -(k - 3)**2 + 3 # -k**2 +6*k - 6
    for k in range(len(p)):
        assert(p[k] == f(k))

    def update_circuit_params(outcome_results, flow_state):
        circuit_params = flow_state['circuit_params']
        k, v = outcome_results
        t = circuit_params['terms']
        t[0] = (t[0][0] - v - 1, [])

    def progress(results, state):
        return results[1] > state['last_good_outcome_results'][1] if state['last_good_outcome_results'][1] else True

    def process_outcome(outcome, state):
        k = int(padded_bin(n_key + n_value, outcome)[n_value:], 2)
        v = int(padded_bin(n_key + n_value, outcome)[:n_value], 2)
        if v >= 2**(n_value - 1):
            v = v - 2**n_value
        v -= state['circuit_params']['terms'][0][0] - state['initial_circuit_params']['terms'][0][0]
        assert(v == p[k])
        return (k, v)

    oracle = oracle_match_0(n_key + n_value, n_key + n_value - 1)

    def build_circuit(flow_state):
        return build_polynomial_circuit(flow_state['circuit_params']['n_key'], flow_state['circuit_params']['n_value'], flow_state['circuit_params']['terms'])

    optimum = grover_optimizer({'n_key': n_key, 'n_value':n_value, 'terms': terms},
                               build_circuit, oracle,
                               update_circuit_params, progress, process_outcome)
    assert(optimum[1] == max(p))
