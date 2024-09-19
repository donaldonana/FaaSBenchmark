import subprocess
import os
import re
import datetime
import swiftclient



def push(chunkdir, ipv4):

    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

	# Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)

    container = 'whiskcontainer'
 
    with open(chunkdir + ".mp4", 'rb') as f:
        conn.put_object(container, chunkdir + ".mp4", contents=f.read())
 
    return ("Ok")


def pull(chunkdir, ipv4):

    chunkdir = chunkdir + ".zip"

    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

    # Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)

    container = 'whiskcontainer'

    obj = conn.get_object(container, chunkdir)
    with open(chunkdir, 'wb') as f:
        f.write(obj[1])

	# unzip the chunk
    args = [
        chunkdir,
		"-d",
        "./"  
    ]
    subprocess.run(
        ["unzip"] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    return ("Ok")


def encode(chunkdir, duration):

    files = os.listdir(chunkdir)   
    pattern = r'frame_(\d+)\.webp'  
    # Extract numbers from filenames that match the pattern
    numbers = [int(re.search(pattern, f).group(1)) for f in files if re.search(pattern, f)]

    if numbers:
        start_number = min(numbers) 
        result = chunkdir+".mp4" 
        chunkdir = chunkdir+"/frame_%004d.webp"
        args = [
            "-framerate",  "6", 
            "-start_number", str(start_number), 
            "-i", chunkdir, 
            "-c:v",  "libx264",
            '-t', str(duration),
            '-pix_fmt', "yuv420p",
            result,
        ]

        process =  subprocess.run(
            ["ffmpeg", '-y'] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        return (process)
    
    else:
        return False


def main(args):

    times = args.get("times")

    duration = times["duration"]

    ipv4 = args.get("ipv4", "192.168.1.120")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, ipv4)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    response = encode(chunkdir, duration)
    process_end = datetime.datetime.now()

    if response:
        push_begin = datetime.datetime.now()
        push(chunkdir, ipv4)
        push_end = datetime.datetime.now()
        push_time = (push_end - push_begin) / datetime.timedelta(seconds=1)
    else: 
        push_time = 0


    times["encode"] = {
        "push" : push_time,
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
        "size" : os.path.getsize(chunkdir+".mp4"),
        # "response" : str(response)
    }
    
    return  times


# ffmpeg -y -framerate 10 -i frame_%004d.webp -c:v libx264 -t 3 -pix_fmt yuv420p output.mp4
