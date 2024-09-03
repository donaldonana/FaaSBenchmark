#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <process> <duration>"
  echo "proc : number of process to run"
  echo "duration : total video duration"
  exit 1
fi

process=$1
duration=$2

chunk_duration=$((duration / process))

wsk action update S1  --sequence decode,scenechange,facerec,draw --timeout 50000

for ((i = 0; i < process; i++)); do

    wsk action invoke S1 -r --blocking \
        --param key $AWS_ACCESS_KEY_ID \
        --param access $AWS_SECRET_ACCESS_KEY \
        --param start $((i * chunk_duration)) \
        --param duration $chunk_duration \
        --param chunkdir "chunk.$i" &
done

wait

echo "All actions have been invoked."
