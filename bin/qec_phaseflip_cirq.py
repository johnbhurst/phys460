#!/usr/bin/env python
# Copyright 2024 John Hurst
# 2024-08-27

import argparse
import math
import matplotlib.pyplot as plt
from cirq import Circuit, CNOT, CCZ, H, LineQubit, measure, ry, Simulator, X, Z

parser = argparse.ArgumentParser(description="Quantum Error Correction: Single bit flip correction.")
# parser.add_argument("--shots", type=int, default=1000, help="Number of shots")
# parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
# parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
parser.add_argument("--theta", type=str, default="0", help="RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X)")
parser.add_argument("--flip", type=int, default=-1, help="Bit to flip: -1 (none), 0, 1, 2")
parser.add_argument("--print", action='store_true', help="Print circuit")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi, "sqrt": math.sqrt, "atan": math.atan}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)

q1, q2, q3 = LineQubit.range(3)
q = [q1, q2, q3]
a1, a2 = LineQubit.range(3, 5)
circuit = Circuit()


# o = ClassicalRegister(3, name='output')
# s = ClassicalRegister(2, name='syndrome')
# circuit = QuantumCircuit(q, a, o, s)

if theta != 0.0:
    # circuit.ry(theta, q1)
    circuit.append(ry(theta)(q1))

# circuit.cx(q1, q2)
# circuit.cx(q1, q3)
circuit.append(CNOT(q1, q2))
circuit.append(CNOT(q1, q3))
circuit.append([H(qx) for qx in q])
if args.unitaryop == 'X':
    # circuit.x(q1)
    # circuit.x(q2)
    # circuit.x(q3)
    circuit.append([Z(qx) for qx in q])
if args.flip != -1:
    # circuit.x(q[args.flip])
    circuit.append(Z(q[args.flip]))
# circuit.cx(q1, a1)
# circuit.cx(q2, a1)
# circuit.cx(q1, a2)
# circuit.cx(q3, a2)
circuit.append([H(qx) for qx in q])
circuit.append(CNOT(q1, a1))
circuit.append(CNOT(q2, a1))
circuit.append(CNOT(q1, a2))
circuit.append(CNOT(q3, a2))
circuit.append([H(qx) for qx in q])
# circuit.mcx([a2, a1], q1, ctrl_state=0b11)
# circuit.mcx([a2, a1], q2, ctrl_state=0b10)
# circuit.mcx([a2, a1], q3, ctrl_state=0b01)
circuit.append(CCZ(a2, a1, q1))
circuit.append(X(a2))
circuit.append(CCZ(a2, a1, q2))
circuit.append(X(a2))
circuit.append(X(a1))
circuit.append(CCZ(a2, a1, q3))
circuit.append(X(a1))
# circuit.cx(q1, q3)
# circuit.cx(q1, q2)
circuit.append([H(qx) for qx in q])
circuit.append(CNOT(q1, q3))
circuit.append(CNOT(q1, q2))
# circuit.measure(q, o)
# circuit.measure(a, s)

if args.print:
    print(circuit)

simulator = Simulator()
result = simulator.simulate(circuit)
print(result)

circuit.append(measure(q1, q2, q3, key='result'))
# samples = simulator.run(circuit, repetitions=args.shots)
# binary_labels = [bin(x)[2:].zfill(2) for x in range(4)]
# plot_state_histogram(samples, plt.subplot(), xlabel = 'measurement state', ylabel = 'count', tick_label=binary_labels)
# if args.filename:
#     plt.savefig(args.filename)
# else:
#     plt.show()

