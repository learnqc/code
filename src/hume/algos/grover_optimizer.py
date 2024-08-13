import copy
from math import pi

from hume.algos.grover import grover_circuit
from hume.simulator.circuit import QuantumRegister, QuantumCircuit
from hume.utils.common import padded_bin


def poly(n_key, terms, pr=False):
    p = [0 for _ in range(2**n_key)]
    for k in range(2**n_key):
        b = padded_bin(n_key, k)
        p_k = 0
        for m in terms:
            p_k_m = m[0]
            for idx in m[1]:
                p_k_m *= int(b[n_key-1-idx])
            p_k += p_k_m
        p[k] = p_k

    if pr:
        print()
        for k in range(2**n_key):
            print(k, '=', b, '-->', p[k])

    return p


def encode_term(coeff, vars, circuit, key, value):
    for i in range(len(value)):
        if len(vars) > 1:
            # circuit.mcp(2*pi * 2 ** (i - N) * coeff, [key[j] for j in vars], value[i])
            circuit.mcp(pi * 2 ** -i * coeff, [key[j] for j in vars], value[i])
        elif len(vars) > 0:
            # circuit.cp(2*pi * 2 ** (i - N) * coeff, key[vars[0]], value[i])
            circuit.cp(pi * 2 ** -i * coeff, key[vars[0]], value[i])
        else:
            # circuit.p(2*pi * 2 ** (i - N) * coeff, value[i])
            circuit.p(pi * 2 ** -i * coeff, value[i])


def build_polynomial_circuit(key_size, value_size, terms):
    key = QuantumRegister(key_size)
    value = QuantumRegister(value_size)
    circuit = QuantumCircuit(key, value)

    for i in range(len(key)):
        circuit.h(key[i])

    for i in range(len(value)):
        circuit.h(value[i])

    for (coeff, vars) in terms:
        encode_term(coeff, vars, circuit, key, value)

    circuit.iqft(value[::-1], swap=False)

    return circuit


def oracle_match_1(bits, tag_bit):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    qc.p(pi, tag_bit)

    return qc


def oracle_match_0(bits, tag_bit):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    qc.x(q[tag_bit])
    qc.p(pi, tag_bit)
    qc.x(q[tag_bit])

    return qc


def grover_optimizer(circuit_params,
                     build_circuit, oracle,
                     update_circuit_params, progress, process_outcome,
                     failure_threshold=7):
    flow_state = {
        'last_good_outcome_results': (None, -1),
        'failure_count': 0,
        'initial_circuit_params': copy.deepcopy(circuit_params),
        'circuit_params': circuit_params
    }

    stop_cond = lambda: flow_state['failure_count'] > failure_threshold
    shots = 100

    def update(outcome_results, flow_state):
        flow_state['last_good_outcome_results'] = outcome_results
        flow_state['failure_count'] = 0
        update_circuit_params(outcome_results, flow_state)

    done = False
    counter = 0
    while not done:
        counter += 1
        for r in [0, 1]:
            print('\niteration', r)
            function = build_circuit(flow_state)
            qc = grover_circuit(function, oracle, r)

            result = qc.measure(shots = shots)

            flow_state['last_run_result'] = result

            outcome = max(result['counts'].items(), key = lambda k: k[1])[0]

            # process outcome
            outcome_results = process_outcome(outcome, flow_state)

            if progress(outcome_results, flow_state):
                print('progress', outcome_results)
                update(outcome_results, flow_state)
                break
            else:
                flow_state['failure_count'] += 1
                print('failure', outcome_results)

                if stop_cond():
                    print('\nSTOPPING WITH OUTCOME RESULTS', flow_state['last_good_outcome_results'])
                    done = True
                    break

    return flow_state['last_good_outcome_results']
