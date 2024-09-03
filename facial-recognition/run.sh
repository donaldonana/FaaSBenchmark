#!/bin/bash

wsk action update S1 --timeout 600000 --sequence decode,scenechange,facerec,draw


# Invoke the OpenWhisk action 'facerec' four times simultaneously
# wsk action invoke facerec --result --param start 00:00:00 --param duration 00:00:06  & 
# wsk action invoke facerec --result --param start 00:00:06 --param duration 00:00:06  & 
# wsk action invoke facerec --result --param start 00:00:12 --param duration 00:00:06  & 
for ((i = 0; i < 8; i++)); do

wsk action invoke S1 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param start $((i * chunk_duration)) --param duration 3 --param chunkdir "chunk.$i" &

done




# Wait for all background processes to complete
wait

echo "All actions have been invoked."