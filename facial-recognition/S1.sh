#!/bin/bash

wsk action update S1 --sequence decode,scenechange,facerec,draw

wsk action invoke S1 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY
