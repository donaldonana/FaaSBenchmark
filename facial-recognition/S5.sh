#!/bin/bash

wsk action update decode --timeout 50000 --memory 512 --docker onanad/action-python-v3.9:decode decode/__main__.py --web true

wsk action update scenechange --timeout 50000 --memory 512 --docker onanad/action-python-v3.9:scenechange scene-change/__main__.py --web true

wsk action update facerec --timeout 600000 --memory 1024 --docker onanad/action-python-v3.9:facerec facial/__main__.py --web true 

wsk action update keep --timeout 50000 --memory 512 --docker onanad/action-python-v3.9:keep keep-scene/__main__.py --web true 

wsk action update facerecprim --timeout 600000 --memory 1024 --docker onanad/action-python-v3.9:facerecprim facial-prim/__main__.py --web true 



wsk action update S5 --sequence decode,scenechange,facerecprim,keep

wsk action invoke S5 -r --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY
