#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <ipv4> <build>"
  echo "ipv4 : ipv4 du swift connection"
  echo "build : Use 'push' or 'pull'. "

  exit 1

fi

ipv4=$1
build=$2

if [ "$build" == "push" ]; then
    docker build -t action-python-v3.9:thumb .
    docker tag action-python-v3.9:thumb onanad/action-python-v3.9:thumb
    docker push onanad/action-python-v3.9:thumb
    wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py --web true
    wsk action invoke thumb --result --param bib pillow --param file 500b.JPEG --param ipv4 "$ipv4"

elif [ "$build" == "pull" ]; then
    docker pull onanad/action-python-v3.9:thumb
    wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py --web true
    wsk action invoke thumb --result --param bib pillow --param file 500b.JPEG --param ipv4 "$ipv4"

else
    echo "Invalid build argument. Use 'push' or 'pull'."
fi
