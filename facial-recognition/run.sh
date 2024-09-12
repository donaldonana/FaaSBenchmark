#!/bin/bash

IPV4="192.168.1.120"
SCHEMA="S9"
VIDEO="queen.mp4"
DURATION=32
PROCESS=10

RESULT_FILE="result/result.txt"
ENERGY_DIR="result/energy"
mkdir -p "$ENERGY_DIR/$SCHEMA"

ENERGY_FILE="$ENERGY_DIR/$SCHEMA/$VIDEO.txt"

./update.sh > /dev/null

for (( i = 1; i <= 1; i++ )); do

    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

        # /bash/$SCHEMA.sh $IPV4 10 $DURATION $SCHEMA $VIDEO  >> $RESULT_FILE
        python3 python/$SCHEMA.py $IPV4 $PROCESS $DURATION $SCHEMA $VIDEO $i  >> $RESULT_FILE

    kill -SIGINT $METER_PID

    echo -e "$i"

    sleep 3
	
done

echo "All actions have been invoked."
