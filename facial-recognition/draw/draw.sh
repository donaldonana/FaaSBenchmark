#!/bin/bash
docker build -t action-python-v3.9:draw .

docker tag action-python-v3.9:draw onanad/action-python-v3.9:draw

docker push onanad/action-python-v3.9:draw

wsk action update draw --memory 128 --docker onanad/action-python-v3.9:draw __main__.py --web true 

# wsk action invoke draw --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY  
