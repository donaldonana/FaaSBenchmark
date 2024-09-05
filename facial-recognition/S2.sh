#!/bin/bash


# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <process> <duration> <schema> <video>"
  echo "proc : number of process to run"
  echo "duration : total video duration"
  echo "schema : schema"
  echo "video : video name"

  exit 1

fi

process=$1
duration=$2
schema=$3
video=$4


chunk_duration=$((duration / process))

wsk action update S2  --sequence decode,facerecprim,draw,encode

for ((i = 0; i < process; i++)); do

    wsk action invoke S2 -r --blocking \
        --param key $AWS_ACCESS_KEY_ID \
        --param access $AWS_SECRET_ACCESS_KEY \
        --param start $((i * chunk_duration)) \
        --param duration $chunk_duration \
        --param schema $schema \
        --param video $video \
        --param chunkdir "chunk.$i" &
done

wait

