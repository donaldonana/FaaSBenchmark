import subprocess
import os
import cv2
import shutil
import datetime
import swiftclient




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

    obj_tuple = conn.get_object(container, chunkdir)
    with open(chunkdir, 'wb') as f:
        f.write(obj_tuple[1])
 
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

 

def keep(ref, chunkdir):

    os.makedirs("newchunkdir", exist_ok=True)

    if ref["scene"]:
        for scene in ref["scenes"]:

            if scene["face"]:

                for file in scene["frames"]:
                    path = os.path.join(chunkdir, file)
                    newpath = os.path.join("newchunkdir", file)
                    frame = cv2.imread(path)
                    cv2.imwrite(newpath, frame)

    else:
        files  = ref["scenes"].keys()

        for file in files:
            path = os.path.join(chunkdir, file)
            newpath = os.path.join("newchunkdir", file)
            frame = cv2.imread(path)
            cv2.imwrite(newpath, frame)

    shutil.rmtree(chunkdir)
    shutil.move("newchunkdir", chunkdir)

    return("Ok")


def main(args):
    
    ipv4 = args.get("ipv4")
    
    ref = args.get("ref")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, ipv4)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    keep(ref, chunkdir)
    process_end = datetime.datetime.now()

    push_begin = datetime.datetime.now()
    push(chunkdir, ipv4)
    push_end = datetime.datetime.now()


    times = args.get("times")

    times["keep"] = {
        "push" : (push_end - push_begin) / datetime.timedelta(seconds=1),
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
    }
    
    return {
        "status" : "Ok",
        "ref" : ref,
        "times" : times,
        "chunkdir": chunkdir,   
        "ipv4" : args.get("ipv4")
    }
