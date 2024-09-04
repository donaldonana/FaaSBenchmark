#!/bin/bash
docker build -t action-python-v3.9:facerecprim .

docker tag action-python-v3.9:facerecprim onanad/action-python-v3.9:facerecprim

docker push onanad/action-python-v3.9:facerecprim

wsk action update facerecprim --timeout 600000 --memory 300 --docker onanad/action-python-v3.9:facerecprim __main__.py --web true 

# wsk action invoke facerecprim --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY 
