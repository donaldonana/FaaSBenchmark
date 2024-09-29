#!/bin/bash
docker build -t action-python-v3.9:text2speech .

docker tag action-python-v3.9:text2speech onanad/action-python-v3.9:text2speech

docker push onanad/action-python-v3.9:text2speech

wsk action update text2speech --memory 128 --docker onanad/action-python-v3.9:text2speech __main__.py --web true 

wsk action invoke text2speech --result  --param ipv4 "192.168.1.120" 


