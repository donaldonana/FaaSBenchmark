import sys
import subprocess
import os


if len(sys.argv) != 2:

    print("Usage: script.py <ipv4> <process> <duration> <schema> <video>")
    print("ipv4 : ipv4 for Swift connection")
    sys.exit(1)

ipv4 = sys.argv[1]
 
os.system("wsk action update S1 --sequence text2speech,conversion > /dev/null")

command = [
        "wsk", "action", "invoke", "S1", "-r", "--blocking",
        "--param", "ipv4", ipv4,
        ]

subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.PIPE, text=True
        )