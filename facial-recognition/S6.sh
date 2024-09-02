#!/bin/bash

 
wsk action update S6 --sequence decode,facerecprim,draw

wsk action invoke S6 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY

