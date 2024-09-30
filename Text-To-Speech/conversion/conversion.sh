#!/bin/bash
docker build --no-cache -t action-python-v3.10:conversion .

docker tag action-python-v3.10:conversion onanad/action-python-v3.10:conversion

docker push onanad/action-python-v3.10:conversion

wsk action update conversion --memory 512 --docker onanad/action-python-v3.10:conversion __main__.py --web true 

wsk action invoke conversion --result  --param ipv4 "192.168.1.120"