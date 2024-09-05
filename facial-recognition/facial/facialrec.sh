#!/bin/bash
docker build -t action-python-v3.9:facerec .

docker tag action-python-v3.9:facerec onanad/action-python-v3.9:facerec

docker push onanad/action-python-v3.9:facerec

wsk action update facerec --memory 256 --docker onanad/action-python-v3.9:facerec __main__.py --web true 

# wsk action invoke facerec --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY 
