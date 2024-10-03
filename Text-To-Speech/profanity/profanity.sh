#!/bin/bash
docker build -t action-python-v3.9:profanity .

docker tag action-python-v3.9:profanity onanad/action-python-v3.9:profanity

docker push onanad/action-python-v3.9:profanity

wsk action update profanity --memory 200 --docker onanad/action-python-v3.9:profanity __main__.py --web true 

wsk action invoke profanity --result  --param ipv4 "130.190.117.182" 

