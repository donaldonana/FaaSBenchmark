import sys
import subprocess
import os


# Check if the correct number of arguments is provided
if len(sys.argv) != 7:

    print("Usage: script.py <ipv4> <process> <duration> <schema> <video>")
    print("ipv4 : ipv4 for Swift connection")
    print("process : number of processes to run")
    print("duration : total video duration")
    print("schema : schema")
    print("video : video name")
    sys.exit(1)

# Assigning the command-line arguments to variables
ipv4     = sys.argv[1]
process  = int(sys.argv[2])
duration = int(sys.argv[3])
schema   = sys.argv[4]
video    = sys.argv[5]
expe     = sys.argv[6]

# update the action
os.system("wsk action update S2  --sequence decode,facerecprim,draw,encode > /dev/null")

processes = []

# Calculate chunk duration
chunk_duration = duration // process

# Loop to invoke the action multiple times in parallel
for i in range(process):   

    start_time = i * chunk_duration
    command = [
        "wsk", "action", "invoke", "S2", "-r", "--blocking",
        "--param", "ipv4", ipv4,
        "--param", "start", str(start_time),
        "--param", "duration", str(chunk_duration),
        "--param", "schema", schema,
        "--param", "video", video,
        "--param", "chunkdir", f"chunk.{i}",
        "--param", "expe", expe
    ]

    # Run each command in the background
    process = subprocess.Popen(command)
    processes.append(process)

# Wait for all processes to complete
for process in processes:
    process.wait()

