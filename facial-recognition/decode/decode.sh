#!/bin/bash
docker build -t action-python-v3.9:decode .

docker tag action-python-v3.9:decode onanad/action-python-v3.9:decode

docker push onanad/action-python-v3.9:decode

wsk action update decode --timeout 50000 --memory 256 --docker onanad/action-python-v3.9:decode __main__.py --web true 

wsk action invoke decode --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY
