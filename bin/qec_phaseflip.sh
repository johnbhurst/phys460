# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

# Run different single qubit phase-flip errors with error correction circuit

SCRIPTDIR=$(dirname "$0")
SCRIPT=${SCRIPTDIR}/qec_phaseflip.py
IMAGEDIR=${SCRIPTDIR}/../images/qec_phaseflip
mkdir -p ${IMAGEDIR}

echo "Input state: |0>, I, no error"
$SCRIPT --filename=$IMAGEDIR/0ket_I_none.png
echo "Input state: |0>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/0ket_I_phase0.png --flip=0
echo "Input state: |0>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/0ket_I_phase1.png --flip=1
echo "Input state: |0>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/0ket_I_phase2.png --flip=2
echo "Input state: |0>, X, no error"
$SCRIPT --filename=$IMAGEDIR/0ket_X_none.png --unitaryop=X
echo "Input state: |0>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/0ket_X_phase0.png --unitaryop=X --flip=0
echo "Input state: |0>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/0ket_X_phase1.png --unitaryop=X --flip=1
echo "Input state: |0>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/0ket_X_phase2.png --unitaryop=X --flip=2

echo "Input state: |1>, I, no error"
$SCRIPT --filename=$IMAGEDIR/1ket_I_none.png --theta=pi
echo "Input state: |1>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/1ket_I_phase0.png --theta=pi --flip=0
echo "Input state: |1>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/1ket_I_phase1.png --theta=pi --flip=1
echo "Input state: |1>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/1ket_I_phase2.png --theta=pi --flip=2
echo "Input state: |1>, X, no error"
$SCRIPT --filename=$IMAGEDIR/1ket_X_none.png --theta=pi --unitaryop=X
echo "Input state: |1>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/1ket_X_phase0.png --theta=pi --unitaryop=X --flip=0
echo "Input state: |1>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/1ket_X_phase1.png --theta=pi --unitaryop=X --flip=1
echo "Input state: |1>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/1ket_X_phase2.png --theta=pi --unitaryop=X --flip=2

echo "Input state: |33:66>, I, no error"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_none.png --theta="2*atan(sqrt(2))"
echo "Input state: |33:66>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_phase0.png --theta="2*atan(sqrt(2))" --flip=0
echo "Input state: |33:66>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_phase1.png --theta="2*atan(sqrt(2))" --flip=1
echo "Input state: |33:66>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_phase2.png --theta="2*atan(sqrt(2))" --flip=2
echo "Input state: |33:66>, X, no error"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_none.png --theta="2*atan(sqrt(2))" --unitaryop=X
echo "Input state: |33:66>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_phase0.png --theta="2*atan(sqrt(2))" --unitaryop=X --flip=0
echo "Input state: |33:66>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_phase1.png --theta="2*atan(sqrt(2))" --unitaryop=X --flip=1
echo "Input state: |33:66>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_phase2.png --theta="2*atan(sqrt(2))" --unitaryop=X --flip=2
