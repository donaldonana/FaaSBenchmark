#!/bin/bash

IMAGE="500b.JPEG"

# The list of library
LIBRARY=("pillow" "wand" "pygame" "opencv")

RESULT_FILE="../result/result.txt"
ENERGY_DIR="../result/energy"
mkdir -p "$ENERGY_DIR/$IMAGE"
 
# Iterate over each libarary in the array
for LIB in "${LIBRARY[@]}"; do

  wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py --web true
  echo -e "$LIB"  
  ENERGY_FILE="$ENERGY_DIR/$IMAGE/$LIB$IMAGE.txt"  
    
  for (( i = 1; i <= 100; i++ )); do
    	 
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

    wsk action invoke thumb -r \
      --param bib "$LIB" \
      --param key $AWS_ACCESS_KEY_ID  \
      --param access $AWS_SECRET_ACCESS_KEY \
      --param file "$IMAGE" >> $RESULT_FILE

    kill -SIGINT $METER_PID
	
  done
    
done
