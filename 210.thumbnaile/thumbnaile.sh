#!/bin/bash

docker build -t action-python-v3.9:thumb .

docker tag action-python-v3.9:thumb onanad/action-python-v3.9:thumb

docker push onanad/action-python-v3.9:thumb

wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py --web true

wsk action invoke thumb  --result  --param bib pillow  --param file 500b.JPEG --param ipv4 "130.190.117.177" 
