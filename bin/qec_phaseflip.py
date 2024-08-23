#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

# See "Quantum Computing and Information: A Scaffolding Approach" by Peter Y Lee, Huiwen Ji, Ran Cheng, Polaris QCI, 2024

import math
from phys460 import get_parser, run_circuit
from qiskit.circuit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import ZGate

parser = get_parser('Quantum Error Correction: Single phase flip correction.')
parser.add_argument("--theta", type=str, default="0", help="RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X)")
parser.add_argument("--flip", type=int, default=-1, help="Bit to flip: -1 (none), 0, 1, 2")
args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi, "sqrt": math.sqrt, "atan": math.atan}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)
q = [q1, q2, q3] = QuantumRegister(3, name='q')
a = [a1, a2] = QuantumRegister(2, name='a')
o = ClassicalRegister(3, name='output')
s = ClassicalRegister(2, name='syndrome')
circuit = QuantumCircuit(q, a, o, s)

if theta != 0.0:
    circuit.ry(theta, q1)
circuit.cx(q1, q2)
circuit.cx(q1, q3)
circuit.h([q1, q2, q3])
circuit.barrier()
if args.unitaryop == 'X':
    circuit.z(q1)
    circuit.z(q2)
    circuit.z(q3)
if args.flip != -1:
    circuit.z(q[args.flip])
circuit.barrier()
circuit.h([q1, q2, q3])
circuit.cx(q1, a1)
circuit.cx(q2, a1)
circuit.cx(q1, a2)
circuit.cx(q3, a2)
circuit.h([q1, q2, q3])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b11), [a2, a1, q1])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b10), [a2, a1, q2])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b01), [a2, a1, q3])
circuit.barrier()
circuit.h([q1, q2, q3])
circuit.cx(q1, q3)
circuit.cx(q1, q2)
circuit.barrier()
circuit.measure(q, o)
circuit.measure(a, s)

result = run_circuit(args, circuit)
syndrome_counts = result[0].data.syndrome.get_counts()
assert len(syndrome_counts) == 1
syndrome = next(iter(syndrome_counts.keys()))
print(f"{syndrome=}")
output_counts = result[0].data.output.get_counts()
for bits, val in sorted(output_counts.items()):
    assert bits[0:2] == "00"
    bit = bits[2]
    print(f"{bit}\t{val}")

