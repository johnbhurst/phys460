# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

import argparse
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2 as FakeProvider
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--provider", type=str, default="aer", help="Provider (aer, fake_manila, fake_kyoto, etc), (default aer)")
    parser.add_argument("--shots", type=int, default=1000, help="Number of shots")
    parser.add_argument("--filename", type=str, help="Filename for circuit diagram")
    parser.add_argument("--isa-filename", type=str, help="Filename for circuit diagram after ISA")
    return parser

def run_circuit(args, circuit):
    if args.filename:
        circuit.draw(output="mpl", filename=args.filename, fold=-1, plot_barriers=False)

    if args.provider == 'aer':
        backend = AerSimulator()
    else:
        backend = next(iter([backend for backend in FakeProvider().backends() if backend.name == args.provider]), None)

    sampler = Sampler(backend)

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    if args.isa_filename:
        isa_circuit.draw(output="mpl", filename=args.isa_filename, fold=-1, plot_barriers=False)

    job = sampler.run([isa_circuit], shots=args.shots)
    return job.result()
