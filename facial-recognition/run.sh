#!/bin/bash


for (( i = 1; i <= 1; i++ )); do

    cpu-energy-meter -r >> energy.txt &
    METER_PID=$!

        ./S9.sh 10 60 "S9" "nature.mp4"

    kill -SIGINT $METER_PID

    echo -e "$i"
	
done