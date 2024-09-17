import subprocess
import os
import cv2
import numpy as np
import datetime
import swiftclient


def pull(chunkdir, ipv4):

    chunkdir = chunkdir + ".zip"
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'
   
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)
   
    container = 'whiskcontainer'
   
    obj_tuple = conn.get_object(container, chunkdir)
   
    with open(chunkdir, 'wb') as f:
        f.write(obj_tuple[1])
        
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


def sceneChange(chunkdir, scene_threshold=0.1):
	
    prev_frame = None
    result = []
    frames = []
    files = sorted([f for f in os.listdir(chunkdir) if f.endswith('.webp')])
	
    for file in files:
        path = os.path.join(chunkdir, file)
        frame = cv2.imread(path)
        
        if prev_frame is not None:
            diff = cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), cv2.cvtColor(prev_frame, cv2.COLOR_RGB2BGR))
			# Normalize the difference to a value between 0 and 1
            normalized_diff = np.sum(diff) / (diff.shape[0] * diff.shape[1] * diff.shape[2] * 255.0)

            if normalized_diff < scene_threshold:
                frames.append(file)
            
            else:
                scene = {"face" : False, "frames" : frames, "box" : []}
                result.append(scene)
                frames = []
                frames.append(file)

        else:
            frames.append(file)

        prev_frame = frame

    scene = {"face" : False, "frames" : frames, "box" : []}
    result.append(scene)

    return result

 
def main(args):
	
    ipv4 = args.get("ipv4")

    chunkdir = args.get("chunkdir", "chunkdir")

    pull_begin = datetime.datetime.now()
    pull(chunkdir, ipv4)
    pull_end = datetime.datetime.now()
    
    process_begin = datetime.datetime.now()
    result = sceneChange(chunkdir)
    process_end = datetime.datetime.now()

    times = args.get("times")

    times["sceneChange"] = {
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
    }
    
    return {
            "status": "OK",
		    "ref" : result,
            "times" : times,
            "chunkdir": chunkdir,
            "ipv4" : ipv4
            }
