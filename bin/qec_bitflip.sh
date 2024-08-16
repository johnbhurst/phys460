# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

# Run different single qubit bit-flip errors with error correction circuit

SCRIPTDIR=$(dirname "$0")
SCRIPT=${SCRIPTDIR}/qec_bitflip.py
IMAGEDIR=${SCRIPTDIR}/../images/qec_bitflip
mkdir -p ${IMAGEDIR}

echo "Input state: |0>, I, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_I_none.png
echo "Input state: |0>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_I_bit0.png --flip=0
echo "Input state: |0>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_I_bit1.png --flip=1
echo "Input state: |0>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_I_bit2.png --flip=2
echo "Input state: |0>, X, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_X_none.png --unitaryop=X
echo "Input state: |0>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_X_bit0.png --unitaryop=X --flip=0
echo "Input state: |0>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_X_bit1.png --unitaryop=X --flip=1
echo "Input state: |0>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_0ket_X_bit2.png --unitaryop=X --flip=2

echo "Input state: |1>, I, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_I_none.png --theta=pi
echo "Input state: |1>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_I_bit0.png --theta=pi --flip=0
echo "Input state: |1>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_I_bit1.png --theta=pi --flip=1
echo "Input state: |1>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_I_bit2.png --theta=pi --flip=2
echo "Input state: |1>, X, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_X_none.png --theta=pi --unitaryop=X
echo "Input state: |1>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_X_bit0.png --theta=pi --unitaryop=X --flip=0
echo "Input state: |1>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_X_bit1.png --theta=pi --unitaryop=X --flip=1
echo "Input state: |1>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_1ket_X_bit2.png --theta=pi --unitaryop=X --flip=2

echo "Input state: |1:2>, I, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_I_none.png --theta=1.231
echo "Input state: |1:2>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_I_bit0.png --theta=1.231 --flip=0
echo "Input state: |1:2>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_I_bit1.png --theta=1.231 --flip=1
echo "Input state: |1:2>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_I_bit2.png --theta=1.231 --flip=2
echo "Input state: |1:2>, X, no error"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_X_none.png --theta=1.231 --unitaryop=X
echo "Input state: |1:2>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_X_bit0.png --theta=1.231 --unitaryop=X --flip=0
echo "Input state: |1:2>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_X_bit1.png --theta=1.231 --unitaryop=X --flip=1
echo "Input state: |1:2>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/bitflip_12ket_X_bit2.png --theta=1.231 --unitaryop=X --flip=2
