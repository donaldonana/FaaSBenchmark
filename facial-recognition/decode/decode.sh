#!/bin/bash
docker build -t action-python-v3.9:decode .

docker tag action-python-v3.9:decode onanad/action-python-v3.9:decode

docker push onanad/action-python-v3.9:decode

wsk action update decode --memory 200 --docker onanad/action-python-v3.9:decode __main__.py --web true 

wsk action invoke decode --result  --param ipv4 "130.190.119.61" 

# wsk action invoke decode --result  --param ipv4 "128.110.96.147" 
