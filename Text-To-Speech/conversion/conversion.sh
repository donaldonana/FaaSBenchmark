#!/bin/bash
docker build -t action-python-v3.9:conversion .

docker tag action-python-v3.9:conversion onanad/action-python-v3.9:conversion

docker push onanad/action-python-v3.9:conversion

wsk action update conversion --memory 200 --docker onanad/action-python-v3.9:conversion __main__.py --web true 

wsk action invoke conversion --result  --param ipv4 "130.190.117.182" 