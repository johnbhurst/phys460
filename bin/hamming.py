#!/usr/bin/env python
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-07-06

# This script demonstrates a simple Hamming(7,4) code.  It encodes a 4-bit input into a 7-bit codeword and decodes a
# 7-bit codeword into a 4-bit output.  It also demonstrates error correction by flipping a single bit in the codeword
# and decoding it.

# See Paul Nahin, "The Logician and the Engineer", Princeton University Press, 2013, p. 132.


def encode(bs):
    # Extract input bits
    x7 = 1 if bs[0] == "1" else 0
    x6 = 1 if bs[1] == "1" else 0
    x5 = 1 if bs[2] == "1" else 0
    x3 = 1 if bs[3] == "1" else 0
    # Parity generator
    x4 = x5 ^ x6 ^ x7
    x2 = x3 ^ x6 ^ x7
    x1 = x3 ^ x5 ^ x7
    # Return result
    return f"{x1}{x2}{x3}{x4}{x5}{x6}{x7}"


def decode(bs):
    # Extract input bits
    x1 = 1 if bs[0] == "1" else 0
    x2 = 1 if bs[1] == "1" else 0
    x3 = 1 if bs[2] == "1" else 0
    x4 = 1 if bs[3] == "1" else 0
    x5 = 1 if bs[4] == "1" else 0
    x6 = 1 if bs[5] == "1" else 0
    x7 = 1 if bs[6] == "1" else 0
    # Syndrome generator
    ɑ = x7 ^ x6 ^ x5 ^ x4
    β = x7 ^ x6 ^ x3 ^ x2
    ɣ = x7 ^ x5 ^ x3 ^ x1
    # Syndrome decoder
    e7 = ɑ and β and ɣ
    e6 = ɑ and β and not ɣ
    e5 = ɑ and not β and ɣ
    e3 = not ɑ and β and ɣ
    # Corrected result
    r7 = x7 ^ e7
    r6 = x6 ^ e6
    r5 = x5 ^ e5
    r3 = x3 ^ e3
    return f"{r7}{r6}{r5}{r3}"


def flip(bs, i):
    b = len(bs) - i - 1
    return bs[:b] + str(1 - int(bs[b])) + bs[b+1:]


for i in range(16):
    bs = f"{i:04b}"
    res = decode(encode(bs))
    if res != bs:
        print(f"{bs} -> {encode(bs)} -> {res}")
    for b in range(4):
        res = decode(flip(encode(bs), b))
        if res != bs:
            print(f"{bs} -> {encode(bs)} -> {flip(encode(bs), b)} -> {res}")
