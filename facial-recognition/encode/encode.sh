#!/bin/bash
docker build -t action-python-v3.9:encode .

docker tag action-python-v3.9:encode onanad/action-python-v3.9:encode

docker push onanad/action-python-v3.9:encode

wsk action update encode --memory 128 --docker onanad/action-python-v3.9:encode __main__.py --web true 

# wsk action invoke encode --result  --param key $AWS_ACCESS_KEY_ID  --param access $AWS_SECRET_ACCESS_KEY  --param chunkdir "chunk.0"


