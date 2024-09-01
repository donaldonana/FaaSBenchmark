#!/bin/bash

# Invoke the OpenWhisk action 'facerec' four times simultaneously
wsk action invoke facerec --result --param start 00:00:00 --param duration 00:00:06  & 
wsk action invoke facerec --result --param start 00:00:06 --param duration 00:00:06  & 
wsk action invoke facerec --result --param start 00:00:12 --param duration 00:00:06  & 



# Wait for all background processes to complete
wait

echo "All actions have been invoked."