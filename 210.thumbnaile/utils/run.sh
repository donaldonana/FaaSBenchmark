#!/bin/bash

if [ "$#" -ne 2 ]; then

  echo "Usage: $0 <ipv4> <image>"
  echo "ipv4 : ipv4 du swift connection"
  echo "image : Use 'push' or 'pull'. "
  exit 1
fi

IPV4=$1

IMAGE=$1

# Library List
LIBRARY=("pillow" "wand" "pygame" "opencv")

RESULT_FILE="../result/result.txt"

ENERGY_DIR="../result/energy"

mkdir -p "$ENERGY_DIR/$IMAGE"
 
 
for LIB in "${LIBRARY[@]}"; do

  echo -e "$LIB"  

  ENERGY_FILE="$ENERGY_DIR/$IMAGE/$LIB$IMAGE.txt"  
    
  for (( i = 1; i <= 100; i++ )); do
    	 
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

    wsk action invoke thumb -r \
      --param bib "$LIB" \
      --param ipv4 "$IPV4" \
      --param file "$IMAGE" >> $RESULT_FILE

    kill -SIGINT $METER_PID
	
  done
    
done
