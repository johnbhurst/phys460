#!/usr/bin/env python
# John Hurst (john.b.hurst@gmail.com)
# 2024-12-30

from qiskit.circuit import QuantumCircuit, QuantumRegister

q = [q0, q1] = QuantumRegister(2, 'q')
circuit = QuantumCircuit(q)
circuit.barrier(label='init')
circuit.h(q0)
circuit.cx(q0, q1)
circuit.barrier(label='final')
circuit.draw(output='mpl', filename='circuit.png')
circuit.draw(output='mpl', filename='circuit_reverse_bits.png', reverse_bits=True)


