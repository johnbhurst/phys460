#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-31
# Demonstrates the Shor 9-qubit quantum error correction code.
# Also shows possible error in [LJC] circuit order.
# See "Quantum Computing and Information: A Scaffolding Approach" by Peter Y Lee, Huiwen Ji, Ran Cheng, Polaris QCI, 2024

import argparse
import cirq
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Quantum Error Correction: Shor 9-qubit correction code.")
parser.add_argument("--theta", type=str, default="0", help="RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X)")
parser.add_argument("--flipbit", type=int, default=-1, help="Bit to bit flip: -1 (none, default), 0-8")
parser.add_argument("--phasebit", type=int, default=-1, help="Bit to phase flip: -1 (none, default), 0-8")
parser.add_argument("--randombit", type=int, default=-1, help="Bit for random rotation: -1 (none, default), 0-8")
parser.add_argument("--ljc", action='store_true', help="Use LJC order for bit flip correction")
parser.add_argument("--print", action='store_true', help="Print circuit")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi, "sqrt": math.sqrt, "atan": math.atan}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)

q1, q2, q3, q4, q5, q6, q7, q8, q9 = cirq.LineQubit.range(9)
q = [q1, q2, q3, q4, q5, q6, q7, q8, q9]
a1, a2, a3, a4, a5, a6, a7, a8 = cirq.LineQubit.range(9, 17)
circuit = cirq.Circuit()

if theta != 0.0:
    circuit.append(cirq.ry(theta)(q1))
# encode phase flip
circuit.append(cirq.CNOT(q1, q4))
circuit.append(cirq.CNOT(q1, q7))
circuit.append(cirq.H(qx) for qx in [q1, q4, q7])
# encode bit flips
circuit.append(cirq.CNOT(q1, q2))
circuit.append(cirq.CNOT(q1, q3))
circuit.append(cirq.CNOT(q4, q5))
circuit.append(cirq.CNOT(q4, q6))
circuit.append(cirq.CNOT(q7, q8))
circuit.append(cirq.CNOT(q7, q9))
if args.unitaryop == 'X':
    circuit.append(cirq.Z(qx) for qx in [q1, q4, q7])
if args.unitaryop == 'Z':
    circuit.append(cirq.X(qx) for qx in [q1, q2, q3])
if args.flipbit != -1:
    circuit.append(cirq.X(q[args.flipbit]))
if args.phasebit != -1:
    circuit.append(cirq.Z(q[args.phasebit]))
# if args.randombit != -1:
    # TODO: random unitary with cirq
    # random_rotation = random_unitary(2)
    # circuit.append(random_rotation, [q[args.randombit]])
# bit flips correction
circuit.append(cirq.CNOT(q1, a1))
circuit.append(cirq.CNOT(q2, a1))
circuit.append(cirq.CNOT(q1, a2))
circuit.append(cirq.CNOT(q3, a2))
circuit.append(cirq.CNOT(q4, a3))
circuit.append(cirq.CNOT(q5, a3))
circuit.append(cirq.CNOT(q4, a4))
circuit.append(cirq.CNOT(q6, a4))
circuit.append(cirq.CNOT(q7, a5))
circuit.append(cirq.CNOT(q8, a5))
circuit.append(cirq.CNOT(q7, a6))
circuit.append(cirq.CNOT(q9, a6))
circuit.append(cirq.CCNOT(a2, a1, q1))
circuit.append(cirq.X(a2))
circuit.append(cirq.CCNOT(a2, a1, q2))
circuit.append(cirq.X(a2))
circuit.append(cirq.X(a1))
circuit.append(cirq.CCNOT(a2, a1, q3))
circuit.append(cirq.X(a1))
circuit.append(cirq.CCNOT(a4, a3, q4))
circuit.append(cirq.X(a4))
circuit.append(cirq.CCNOT(a4, a3, q5))
circuit.append(cirq.X(a4))
circuit.append(cirq.X(a3))
circuit.append(cirq.CCNOT(a4, a3, q6))
circuit.append(cirq.X(a3))
circuit.append(cirq.CCNOT(a6, a5, q7))
circuit.append(cirq.X(a6))
circuit.append(cirq.CCNOT(a6, a5, q8))
circuit.append(cirq.X(a6))
circuit.append(cirq.X(a5))
circuit.append(cirq.CCNOT(a6, a5, q9))
circuit.append(cirq.X(a5))
# decode bitflips: note this is in a different order from [LJC].
if not args.ljc:
    circuit.append(cirq.CNOT(q7, q9))
    circuit.append(cirq.CNOT(q7, q8))
    circuit.append(cirq.CNOT(q4, q6))
    circuit.append(cirq.CNOT(q4, q5))
    circuit.append(cirq.CNOT(q1, q3))
    circuit.append(cirq.CNOT(q1, q2))
# phase flip correction
circuit.append(cirq.H(qx) for qx in [q1, q4, q7])
circuit.append(cirq.CNOT(q1, a7))
circuit.append(cirq.CNOT(q4, a7))
circuit.append(cirq.CNOT(q1, a8))
circuit.append(cirq.CNOT(q7, a8))
circuit.append(cirq.H(qx) for qx in [q1, q4, q7])
circuit.append(cirq.CCZ(a8, a7, q1))
circuit.append(cirq.X(a8))
circuit.append(cirq.CCZ(a8, a7, q4))
circuit.append(cirq.X(a8))
circuit.append(cirq.X(a7))
circuit.append(cirq.CCZ(a8, a7, q7))
circuit.append(cirq.X(a7))
# decode bitflips: note this is in a different order from [LJC].
if args.ljc:
    circuit.append(cirq.CNOT(q7, q9))
    circuit.append(cirq.CNOT(q7, q8))
    circuit.append(cirq.CNOT(q4, q6))
    circuit.append(cirq.CNOT(q4, q5))
    circuit.append(cirq.CNOT(q1, q3))
    circuit.append(cirq.CNOT(q1, q2))
# decode phase flip
circuit.append(cirq.H(qx) for qx in [q1, q4, q7])
circuit.append(cirq.CNOT(q1, q7))
circuit.append(cirq.CNOT(q1, q4))
circuit.append(cirq.measure(q1, q2, q3, q4, q5, q6, q7, q8, q9, key='result'))
circuit.append(cirq.measure(a1, a2, a3, a4,  a5, a6, a7, a8, key='syndrome'))

if args.print:
    print(circuit)

simulator = cirq.Simulator()
result = simulator.simulate(circuit)
measurements = result.measurements
def numpy_array_to_bitstring(array):
    return ''.join(str(bit) for bit in array)[::-1]

for key, value in measurements.items():
    bitstring = numpy_array_to_bitstring(value.flatten())
    print(f"{key}: {bitstring}")

# samples = simulator.run(circuit, repetitions=args.shots)
# binary_labels = [bin(x)[2:].zfill(2) for x in range(4)]
# cirq.plot_state_histogram(samples, plt.subplot(), xlabel = 'measurement state', ylabel = 'count', tick_label=binary_labels)
# if args.filename:
#     plt.savefig(args.filename)
# else:
#     plt.show()

