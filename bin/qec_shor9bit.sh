#!/usr/bin/env bash
# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

# Run different single qubit bit-flip errors with error correction circuit

SCRIPTDIR=$(dirname "$0")
SCRIPT=${SCRIPTDIR}/qec_shor9bit.py
IMAGEDIR=${SCRIPTDIR}/../images/qec_shor9bit
mkdir -p ${IMAGEDIR}

function run {
    local description=$1
    shift
    local filename=$1
    shift
    echo $description
    $SCRIPT --filename=$IMAGEDIR/$filename $@
    echo ""
}

function runsetup() {
    local inputstate=$1
    shift
    local ketname=$1
    shift
    local ry=$1
    shift
    local unitaryop
    for unitaryop in "I" "X" "Z"; do
        # run with no errors
        run "Input state: ${inputstate}, ${unitaryop}, no error" "${ketname}_${unitaryop}_none.png" --ry=$ry --unitaryop=$unitaryop
        # run with each of 9 bit flips
        for B in $(seq 0 8); do
            run "Input state: ${inputstate}, ${unitaryop}, flip bit ${B}" "${ketname}_${unitaryop}_bit${B}.png" --ry=$ry --unitaryop=$unitaryop --flipbit=$B
        done
        # run with each of 9 phase flips
        for B in $(seq 0 8); do
            run "Input state: ${inputstate}, ${unitaryop}, flip phase ${B}" "${ketname}_${unitaryop}_phase${B}.png" --ry=$ry --unitaryop=$unitaryop --phasebit=$B
        done
        for B in $(seq 0 8); do
            run "Input state: ${inputstate}, ${unitaryop}, random rotation on bit ${B}" "${ketname}_${unitaryop}_random${B}.png" --ry=$ry --unitaryop=$unitaryop --randombit=$B
        done
    done
}

runsetup "|0>" "0ket" "0"
runsetup "|1>" "1ket" "pi"
runsetup "|33:66>" "3366ket" "2*atan(sqrt(2))"

