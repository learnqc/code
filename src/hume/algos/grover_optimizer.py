import copy
from math import pi

from hume import QuantumRegister, QuantumCircuit
from hume.algos.grover import grover_circuit


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


def oracle_match_0_multi(bits, tag_bits):
    q = QuantumRegister(bits)
    qc = QuantumCircuit(q)

    for t in tag_bits:
        qc.x(q[t])

    qc.mcp(pi, [q[t] for t in tag_bits[:-1]], q[len(q) - 1])

    for t in tag_bits:
        qc.x(q[t])

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

