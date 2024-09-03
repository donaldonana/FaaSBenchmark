#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <num_processes> <video_time>"
  exit 1
fi

num_processes=$1
video_time=$2


wsk action update S1 --sequence decode

chunk_duration=$((video_time / num_processes))

for ((i = 0; i < num_processes; i++)); do

  start_time=$((i * chunk_duration))

  if [ $i -eq $((num_processes - 1)) ]; then
    duration=$((video_time - start_time))

  else
    duration=$chunk_duration
    
  fi
  
  wsk action invoke S1 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param start $start_time --param duration $duration --param chunkdir "chunk.$i" &
  sleep 1
  echo "Started process $i for chunk starting at $start_time with duration $duration" 

done

wait

echo "All video chunks have been processed."



# wsk action update S1.$i   --sequence decode
#   wsk action update decode.$i --timeout 50000  --memory 512 --docker onanad/action-python-v3.9:decode.$i decode/__main__.py --web true



