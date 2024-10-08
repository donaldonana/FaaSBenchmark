#!/bin/bash
docker build -t action-python-v3.9:validation .

docker tag action-python-v3.9:validation onanad/action-python-v3.9:validation

docker push onanad/action-python-v3.9:validation

wsk action update validation --docker onanad/action-python-v3.9:validation __main__.py --web true 

wsk action invoke validation --result  --param ipv4 "130.190.117.182" 

