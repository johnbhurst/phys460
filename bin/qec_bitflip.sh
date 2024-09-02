# Copyright 2024 John Hurst
# John Hurst (john.b.hurst@gmail.com)
# 2024-08-17

# Run different single qubit bit-flip errors with error correction circuit

SCRIPTDIR=$(dirname "$0")
SCRIPT=${SCRIPTDIR}/qec_bitflip.py
IMAGEDIR=${SCRIPTDIR}/../images/qec_bitflip
mkdir -p ${IMAGEDIR}

echo "Input state: |0>, I, no error"
$SCRIPT --filename=$IMAGEDIR/0ket_I_none.png
echo "Input state: |0>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/0ket_I_bit0.png --flip=0
echo "Input state: |0>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/0ket_I_bit1.png --flip=1
echo "Input state: |0>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/0ket_I_bit2.png --flip=2
echo "Input state: |0>, X, no error"
$SCRIPT --filename=$IMAGEDIR/0ket_X_none.png --unitaryop=X
echo "Input state: |0>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/0ket_X_bit0.png --unitaryop=X --flip=0
echo "Input state: |0>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/0ket_X_bit1.png --unitaryop=X --flip=1
echo "Input state: |0>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/0ket_X_bit2.png --unitaryop=X --flip=2

echo "Input state: |1>, I, no error"
$SCRIPT --filename=$IMAGEDIR/1ket_I_none.png --ry=pi
echo "Input state: |1>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/1ket_I_bit0.png --ry=pi --flip=0
echo "Input state: |1>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/1ket_I_bit1.png --ry=pi --flip=1
echo "Input state: |1>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/1ket_I_bit2.png --ry=pi --flip=2
echo "Input state: |1>, X, no error"
$SCRIPT --filename=$IMAGEDIR/1ket_X_none.png --ry=pi --unitaryop=X
echo "Input state: |1>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/1ket_X_bit0.png --ry=pi --unitaryop=X --flip=0
echo "Input state: |1>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/1ket_X_bit1.png --ry=pi --unitaryop=X --flip=1
echo "Input state: |1>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/1ket_X_bit2.png --ry=pi --unitaryop=X --flip=2

echo "Input state: |33:66>, I, no error"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_none.png --ry="2*atan(sqrt(2))"
echo "Input state: |33:66>, I, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_bit0.png --ry="2*atan(sqrt(2))" --flip=0
echo "Input state: |33:66>, I, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_bit1.png --ry="2*atan(sqrt(2))" --flip=1
echo "Input state: |33:66>, I, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/3366ket_I_bit2.png --ry="2*atan(sqrt(2))" --flip=2
echo "Input state: |33:66>, X, no error"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_none.png --ry="2*atan(sqrt(2))" --unitaryop=X
echo "Input state: |33:66>, X, flip bit 0"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_bit0.png --ry="2*atan(sqrt(2))" --unitaryop=X --flip=0
echo "Input state: |33:66>, X, flip bit 1"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_bit1.png --ry="2*atan(sqrt(2))" --unitaryop=X --flip=1
echo "Input state: |33:66>, X, flip bit 2"
$SCRIPT --filename=$IMAGEDIR/3366ket_X_bit2.png --ry="2*atan(sqrt(2))" --unitaryop=X --flip=2
