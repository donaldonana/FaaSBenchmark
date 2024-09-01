#!/bin/bash

 
wsk action update S1 --sequence decode,facerecprim,draw

wsk action invoke S1 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY

echo "All actions have been invoked."
