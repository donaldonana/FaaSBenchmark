#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <ipv4> <process> <duration> <schema> <video>"
  echo "ipv4 : ipv4 du swift connection"
  echo "proc : number of process to run"
  echo "duration : total video duration"
  echo "schema : schema"
  echo "video : video name"

  exit 1

fi

ipv4=$1
process=$2
duration=$3
schema=$4
video=$5


chunk_duration=$((duration / process))

wsk action update S4  --sequence decode,scenechange,facerecprim,keep,encode  > /dev/null

for ((i = 0; i < process; i++)); do

    wsk action invoke S4 -r --blocking \
        --param ipv4 $ipv4 \
        --param start $((i * chunk_duration)) \
        --param duration $chunk_duration \
        --param schema $schema \
        --param video $video \
        --param chunkdir "chunk.$i" &
done

wait
 