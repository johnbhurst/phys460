#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-16

# See "Quantum Computing and Information: A Scaffolding Approach" by Peter Y Lee, Huiwen Ji, Ran Cheng, Polaris QCI, 2024

import math
import numpy
from phys460 import get_parser, run_circuit
from qiskit.circuit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import ZGate
from qiskit.quantum_info import Pauli, random_unitary

parser = get_parser('Quantum Error Correction: Shor 9-qubit correction code.')
parser.add_argument("--ry", type=str, default="0", help="Initialization RY rotation angle (e.g. 'pi', '2*atan(sqrt(2))')")
parser.add_argument("--unitaryop", type=str, default="I", help="Unitary operation (I, X, Z)")
parser.add_argument("--xbit", type=int, default=-1, help="Bit to apply X (bit flip noise) on: -1 (none, default), 0-8")
parser.add_argument("--ybit", type=int, default=-1, help="Bit to apply Y (bit flip noise) on: -1 (none, default), 0-8")
parser.add_argument("--zbit", type=int, default=-1, help="Bit to apply Z (phase flip noise) on: -1 (none, default), 0-8")
parser.add_argument("--xybit", type=int, default=-1, help="Bit to apply superposition 1/√2(X+Y) (mixed noise) on: -1 (none, default), 0-8")
parser.add_argument("--xzbit", type=int, default=-1, help="Bit to apply superposition 1/√2(X+Z) (mixed noise) on: -1 (none, default), 0-8")
parser.add_argument("--yzbit", type=int, default=-1, help="Bit to apply superposition 1/√2(Y+Z) (mixed noise) on: -1 (none, default), 0-8")
parser.add_argument("--randombit", type=int, default=-1, help="Bit to apply random rotation (noise) on: -1 (none, default), 0-8")
parser.add_argument("--ljc", action='store_true', help="Use LJC order for bit flip correction")

args = parser.parse_args()

def safe_eval(expr):
    allowed_names = {"pi": math.pi, "sqrt": math.sqrt, "atan": math.atan}
    return eval(expr, {"__builtins__": None}, allowed_names)

ry = safe_eval(args.ry)
X = Pauli('X').to_matrix()
Y = Pauli('Y').to_matrix()
Z = Pauli('Z').to_matrix()
supXY = (X + Y) / math.sqrt(2)
supXZ = (X + Z) / math.sqrt(2)
supYZ = (Y + Z) / math.sqrt(2)

q = [q1, q2, q3, q4, q5, q6, q7, q8, q9] = QuantumRegister(9, name='q')
a = [a1, a2, a3, a4, a5, a6, a7, a8] = QuantumRegister(8, name='a')
o = ClassicalRegister(9, name='output')
s = ClassicalRegister(8, name='syndrome')
circuit = QuantumCircuit(q, a, o, s)

if ry != 0.0:
    circuit.ry(ry, q1)
# encode phase flip
circuit.cx(q1, q4)
circuit.cx(q1, q7)
circuit.h([q1, q4, q7])
# encode bit flips
circuit.cx(q1, q2)
circuit.cx(q1, q3)
circuit.cx(q4, q5)
circuit.cx(q4, q6)
circuit.cx(q7, q8)
circuit.cx(q7, q9)
circuit.barrier()
if args.unitaryop == 'X':
    circuit.z(q1)
    circuit.z(q4)
    circuit.z(q7)
if args.unitaryop == 'Z':
    circuit.x(q1)
    circuit.x(q2)
    circuit.x(q3)
circuit.barrier()
if args.xbit != -1:
    circuit.x(q[args.xbit])
if args.ybit != -1:
    circuit.y(q[args.ybit])
if args.zbit != -1:
    circuit.z(q[args.zbit])
if args.xybit != -1:
    circuit.unitary(supXY, [q[args.xybit]])
if args.xzbit != -1:
    circuit.unitary(supXZ, [q[args.xzbit]])
if args.yzbit != -1:
    circuit.unitary(supYZ, [q[args.yzbit]])
if args.randombit != -1:
    random_rotation = random_unitary(2)
    circuit.append(random_rotation, [q[args.randombit]])
circuit.barrier()
# bit flips correction
circuit.cx(q1, a1)
circuit.cx(q2, a1)
circuit.cx(q1, a2)
circuit.cx(q3, a2)
circuit.barrier()
circuit.cx(q4, a3)
circuit.cx(q5, a3)
circuit.cx(q4, a4)
circuit.cx(q6, a4)
circuit.barrier()
circuit.cx(q7, a5)
circuit.cx(q8, a5)
circuit.cx(q7, a6)
circuit.cx(q9, a6)
circuit.barrier()
circuit.mcx([a2, a1], q1, ctrl_state=0b11)
circuit.mcx([a2, a1], q2, ctrl_state=0b10)
circuit.mcx([a2, a1], q3, ctrl_state=0b01)
circuit.barrier()
circuit.mcx([a4, a3], q4, ctrl_state=0b11)
circuit.mcx([a4, a3], q5, ctrl_state=0b10)
circuit.mcx([a4, a3], q6, ctrl_state=0b01)
circuit.barrier()
circuit.mcx([a6, a5], q7, ctrl_state=0b11)
circuit.mcx([a6, a5], q8, ctrl_state=0b10)
circuit.mcx([a6, a5], q9, ctrl_state=0b01)
circuit.barrier()
# decode bitflips: note this is in a different order from [LJC].
if not args.ljc:
    circuit.cx(q7, q9)
    circuit.cx(q7, q8)
    circuit.cx(q4, q6)
    circuit.cx(q4, q5)
    circuit.cx(q1, q3)
    circuit.cx(q1, q2)
    circuit.barrier()
# phase flip correction
circuit.h([q1, q4, q7])
circuit.cx(q1, a7)
circuit.cx(q4, a7)
circuit.cx(q1, a8)
circuit.cx(q7, a8)
circuit.barrier()
circuit.h([q1, q4, q7])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b11), [a8, a7, q1])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b10), [a8, a7, q4])
circuit.append(ZGate().control(num_ctrl_qubits=2, ctrl_state=0b01), [a8, a7, q7])
circuit.barrier()
# decode bitflips: note this is in a different order from [LJC].
if args.ljc:
    circuit.cx(q7, q9)
    circuit.cx(q7, q8)
    circuit.cx(q4, q6)
    circuit.cx(q4, q5)
    circuit.cx(q1, q3)
    circuit.cx(q1, q2)
    circuit.barrier()
# decode phase flip
circuit.h([q1, q4, q7])
circuit.cx(q1, q7)
circuit.cx(q1, q4)
circuit.barrier()
circuit.measure(q, o)
circuit.measure(a, s)

result = run_circuit(args, circuit)
syndrome_counts = result[0].data.syndrome.get_counts()
if not args.ljc and args.randombit == -1 and args.xzbit == -1 and args.xybit == -1 and args.yzbit == -1:
    assert len(syndrome_counts) == 1
print("Syndromes:")
for bits, val in sorted(syndrome_counts.items()):
    print(f"{bits}\t{val}")
output_counts = result[0].data.output.get_counts()
print("Output:")
for bits, val in sorted(output_counts.items()):
    if not args.ljc:
        assert bits[0:8] == "00000000"
    bit = bits[8]
    print(f"{bit}\t{val}")
