#!/bin/bash
docker build -t action-python-v3.9:censor .

docker tag action-python-v3.9:censor onanad/action-python-v3.9:censor

docker push onanad/action-python-v3.9:censor

wsk action update censor --memory 300 --docker onanad/action-python-v3.9:censor __main__.py --web true 

wsk action invoke censor --result  --param ipv4 "130.190.117.182" 