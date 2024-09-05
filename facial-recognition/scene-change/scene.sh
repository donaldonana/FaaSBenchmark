#!/bin/bash
docker build -t action-python-v3.9:scenechange .

docker tag action-python-v3.9:scenechange onanad/action-python-v3.9:scenechange

docker push onanad/action-python-v3.9:scenechange

wsk action update scenechange --memory 200 --docker onanad/action-python-v3.9:scenechange __main__.py --web true 

# wsk action invoke scenechange --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY  
