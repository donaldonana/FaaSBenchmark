#!/bin/bash

wsk action update S1 --timeout 600000 --sequence decode,scenechange,facerec,draw

for ((i = 0; i < 8; i++)); do

    wsk action invoke S1 -r \
        --param key $AWS_ACCESS_KEY_ID \
        --param access $AWS_SECRET_ACCESS_KEY \
        --param start $((i * chunk_duration)) \
        --param duration 2 \
        --param chunkdir "chunk.$i" &


done

wait

echo "All actions have been invoked."