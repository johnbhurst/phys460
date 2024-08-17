#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-16

import argparse
import math
from qiskit import  ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.circuit.library import QFT, RYGate, UnitaryGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

parser = argparse.ArgumentParser(description='Shor 9-qubit error correcting code.')
parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
parser.add_argument("--theta", type=str, default="pi/2", help="RY rotation angle (e.g. 'pi/2')")
parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
args = parser.parse_args()


def safe_eval(expr):
    allowed_names = {"pi": math.pi}
    return eval(expr, {"__builtins__": None}, allowed_names)

theta = safe_eval(args.theta)


# Set up circuit

qr = QuantumRegister(3, 'q')
cr = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qr, cr)
circuit.ry(theta, qr[0])
circuit.h(qr[1])
circuit.cx(qr[1], qr[2])
circuit.cx(qr[0], qr[1])
circuit.h(qr[0])
circuit.cx(qr[1], qr[2])
circuit.cz(qr[0], qr[2])
circuit.measure(qr, cr)

# Output and run:
if args.filename:
    circuit.draw(output="mpl", filename=args.filename)

if args.provider == 'aer':
    backend = AerSimulator()
else:
    backend = next(iter([backend for backend in FakeProvider().backends() if backend.name == args.provider]), None)

sampler = Sampler(backend)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(circuit)

if args.isa_filename:
    isa_circuit.draw(output="mpl", filename=args.isa_filename)

job = sampler.run([isa_circuit], shots=args.shots)
result = job.result()
counts = result[0].data.c.get_counts()

for bits, val in sorted(counts.items()):
    print(f"{bits}\t{val}")

