#!/bin/bash

SCHEMA="S3"
VIDEO="queen.mp4"
DURATION=60

RESULT_FILE="result/result.txt"
RESULT_FILE="result/result.txt"
ENERGY_DIR="result/energy"
mkdir -p "$ENERGY_DIR/$SCHEMA"

ENERGY_FILE="$ENERGY_DIR/$SCHEMA/$VIDEO.txt"

wsk action update decode  --memory 200 --docker onanad/action-python-v3.9:decode decode/__main__.py --web true 
wsk action update draw    --memory 128 --docker onanad/action-python-v3.9:draw   draw/__main__.py --web true 
wsk action update encode  --memory 128 --docker onanad/action-python-v3.9:encode encode/__main__.py --web true 
wsk action update facerec --memory 256 --docker onanad/action-python-v3.9:facerec facial/__main__.py --web true 
wsk action update facerecprim --memory 300 --docker onanad/action-python-v3.9:facerecprim facial-prim/__main__.py --web true 
wsk action update keep --memory 200 --docker onanad/action-python-v3.9:keep keep-scene/__main__.py --web true 
wsk action update scenechange --memory 200 --docker onanad/action-python-v3.9:scenechange scene-change/__main__.py --web true 


for (( i = 1; i <= 1; i++ )); do

    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

        ./$SCHEMA.sh 10 $DURATION $SCHEMA $VIDEO  >> $RESULT_FILE

    kill -SIGINT $METER_PID

    echo -e "$i"
	
done

echo "All actions have been invoked."
