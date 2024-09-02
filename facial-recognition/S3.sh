#!/bin/bash

wsk action update S3 --sequence decode,scenechange,facerecprim,draw

wsk action invoke S3 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY
