#!/bin/bash

SCHEMA="S3"
VIDEO="queen.mp4"
DURATION=60

RESULT_FILE="result/result.txt"
RESULT_FILE="result/result.txt"
ENERGY_DIR="result/energy"
mkdir -p "$ENERGY_DIR/$SCHEMA"

ENERGY_FILE="$ENERGY_DIR/$SCHEMA/$VIDEO.txt"

for (( i = 1; i <= 1; i++ )); do

    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

        ./$SCHEMA.sh 10 $DURATION $SCHEMA $VIDEO  >> $RESULT_FILE

    kill -SIGINT $METER_PID

    echo -e "$i"
	
done

echo "All actions have been invoked."
