#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-16

import math
from phys460 import get_parser, run_circuit
from qiskit.circuit import  ClassicalRegister, QuantumCircuit, QuantumRegister

parser = get_parser('Quantum Error Correction: Single bit flip correction.')
parser.add_argument("--theta", type=str, default="0", help="RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X)")
parser.add_argument("--flip", type=int, default=-1, help="Bit to flip: -1 (none), 0, 1, 2")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)
q = [q1, q2, q3] = QuantumRegister(3, name='q')
a = [a1, a2] = QuantumRegister(2, name='a')
c = ClassicalRegister(3, name='c')
s = ClassicalRegister(2, name='syndrome')
circuit = QuantumCircuit(q, a, c, s)

circuit.ry(theta, q1)
circuit.cx(q1, q2)
circuit.cx(q1, q3)
if args.unitaryop == 'X':
    circuit.x(q1)
    circuit.x(q2)
    circuit.x(q3)
if args.flip != -1:
    circuit.x(q[args.flip])
circuit.cx(q1, a1)
circuit.cx(q2, a1)
circuit.cx(q1, a2)
circuit.cx(q3, a2)
circuit.mcx([a2, a1], q1, ctrl_state=0b11)
circuit.mcx([a2, a1], q2, ctrl_state=0b10)
circuit.mcx([a2, a1], q3, ctrl_state=0b01)
circuit.cx(q1, q3)
circuit.cx(q1, q2)
circuit.measure(q, c)
circuit.measure(a, s)

result = run_circuit(args, circuit)
counts = result[0].data.c.get_counts()
syndrome_counts = result[0].data.syndrome.get_counts()
assert len(syndrome_counts) == 1
syndrome = next(iter(syndrome_counts.keys()))
print(f"{syndrome=}")
for bits, val in sorted(counts.items()):
    assert bits[0:2] == "00"
    bit = bits[2]
    print(f"{bit}\t{val}")

