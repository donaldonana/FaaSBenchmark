#!/bin/bash

wsk action update S4 --sequence decode,scenechange,facerecprim,keep

wsk action invoke S4 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY
