#!/usr/bin/env python
# Copyright 2024 John Hurst
# 2024-08-27

import argparse
import math
import matplotlib.pyplot as plt
from cirq import CCNOT, Circuit, CNOT, LineQubit, measure, ry, Simulator, X

parser = argparse.ArgumentParser(description="Quantum Error Correction: Single bit flip correction.")
parser.add_argument("--ry", type=str, default="0", help="Initialization RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X)")
parser.add_argument("--flip", type=int, default=-1, help="Bit to flip: -1 (none), 0, 1, 2")
parser.add_argument("--print", action='store_true', help="Print circuit")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi, "sqrt": math.sqrt, "atan": math.atan}
    return eval(expr, {"__builtins__": None}, allowed_names)

ry = safe_eval(args.ry)

q1, q2, q3 = LineQubit.range(3)
q = [q1, q2, q3]
a1, a2 = LineQubit.range(3, 5)
circuit = Circuit()

if ry != 0.0:
    circuit.append(ry(ry)(q1))

circuit.append(CNOT(q1, q2))
circuit.append(CNOT(q1, q3))
if args.unitaryop == 'X':
    circuit.append(X(q1))
    circuit.append(X(q2))
    circuit.append(X(q3))
if args.flip != -1:
    circuit.append(X(q[args.flip]))
circuit.append(CNOT(q1, a1))
circuit.append(CNOT(q2, a1))
circuit.append(CNOT(q1, a2))
circuit.append(CNOT(q3, a2))
circuit.append(CCNOT(a2, a1, q1))
circuit.append(X(a2))
circuit.append(CCNOT(a2, a1, q2))
circuit.append(X(a2))
circuit.append(X(a1))
circuit.append(CCNOT(a2, a1, q3))
circuit.append(X(a1))
circuit.append(CNOT(q1, q3))
circuit.append(CNOT(q1, q2))
circuit.append(measure(q1, q2, q3, key='result'))
circuit.append(measure(a1, a2, key='syndrome'))

if args.print:
    print(circuit)

simulator = Simulator()
result = simulator.simulate(circuit)
measurements = result.measurements
def numpy_array_to_bitstring(array):
    return ''.join(str(bit) for bit in array)[::-1]

for key, value in measurements.items():
    bitstring = numpy_array_to_bitstring(value.flatten())
    print(f"{key}: {bitstring}")

# samples = simulator.run(circuit, repetitions=args.shots)
# binary_labels = [bin(x)[2:].zfill(2) for x in range(4)]
# plot_state_histogram(samples, plt.subplot(), xlabel = 'measurement state', ylabel = 'count', tick_label=binary_labels)
# if args.filename:
#     plt.savefig(args.filename)
# else:
#     plt.show()

