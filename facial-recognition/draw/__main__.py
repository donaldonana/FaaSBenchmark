import subprocess
import os
import cv2
import swiftclient
import datetime



def push(chunkdir, ipv4):

    os.remove(chunkdir + ".zip")
    args = [
        chunkdir + ".zip", 
        chunkdir  
    ]
    subprocess.run(
        ["zip", '-r'] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

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

    with open(chunkdir + ".zip", 'rb') as f:
        conn.put_object(container, chunkdir + ".zip", contents=f.read())
 
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
 

def draw(ref, chunkdir):

    if ref["scene"]:
        for scene in ref["scenes"]:
            
            if scene["face"]:
                box = scene["box"]
                for file in scene["frames"]:
                    path = os.path.join(chunkdir, file)
                    frame = cv2.imread(path)
                    cv2.rectangle(frame,  (box[0][0], box[0][1]) ,  (box[1][0], box[1][1]) , (0, 255, 0), 2)
                    cv2.imwrite(path, frame)
            # else :
            #     for file in scene["frames"]:
            #         path = os.path.join(chunkdir, file)
            #         frame = cv2.imread(path)
            #         cv2.imwrite(newpath, frame)

    else:
        files  = ref["scenes"].keys()

        for file in files:
            path = os.path.join(chunkdir, file)
            frame = cv2.imread(path)
            box = ref["scenes"][file]
            cv2.rectangle(frame,  (box[0][0], box[0][1]) ,  (box[1][0], box[1][1]) , (0, 255, 0), 2)
            cv2.imwrite(path, frame)

    return("Ok")


def main(args):
    
    ipv4 = args.get("ipv4", "192.168.1.120")
    
    ref = args.get("ref")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, ipv4)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    draw(ref, chunkdir)
    process_end = datetime.datetime.now()

    push_begin = datetime.datetime.now()
    push(chunkdir, ipv4)
    push_end = datetime.datetime.now()

    times = args.get("times")

    times["draw"] = {
        "push" : (push_end - push_begin) / datetime.timedelta(seconds=1),
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
    }

    
    return {
        "status" : "Ok",
        "ref" : ref,
        "times" : times,
        "chunkdir": chunkdir,   
        "ipv4" : ipv4,
    }
