import subprocess
import os
import cv2
import numpy as np
import boto3
 

def pull(chunkdir, key, access):

    chunkdir = chunkdir + ".zip"
    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
    # pull chunk from amazone S3
    s3.download_file(bucket_name, chunkdir, chunkdir)
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


def sceneChange(chunkdir, scene_threshold=0.1):
	
    prev_frame = None
    result = []
    frames = []
    files = sorted([f for f in os.listdir(chunkdir) if f.endswith('.png')])
	
    for file in files:
        path = os.path.join(chunkdir, file)
        frame = cv2.imread(path)
        
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
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
	
    key = args.get("key")

    access = args.get("access")

    chunkdir = args.get("chunkdir", "chunkdir")

    pull(chunkdir, key, access)
    
    result = sceneChange(chunkdir)
    
    return {
            "status": "OK",
		    "ref" : result,
            "chunkdir": chunkdir,
            "key" : args.get("key"),
            "access" : args.get("access")
            }
