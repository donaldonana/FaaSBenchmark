#!/bin/bash
docker build -t action-python-v3.9:keep .

docker tag action-python-v3.9:keep onanad/action-python-v3.9:keep

docker push onanad/action-python-v3.9:keep

wsk action update keep --memory 200 --docker onanad/action-python-v3.9:keep __main__.py --web true 

# wsk action invoke keep --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY -P ../save.json
