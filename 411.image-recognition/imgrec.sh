#!/bin/bash

docker build -t action-python-v3.9:imgrec .

docker tag action-python-v3.9:imgrec onanad/action-python-v3.9:imgrec

docker push onanad/action-python-v3.9:imgrec

wsk action update imgrec --timeout 300000 --memory 1024 --docker onanad/action-python-v3.9:imgrec __main__.py --web true 

wsk action invoke imgrec --result --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY --param image 1Mb.JPEG --param resnet resnet18
