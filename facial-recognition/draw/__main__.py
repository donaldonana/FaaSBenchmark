import subprocess
import os
import cv2
import numpy as np
import boto3

def push(framedir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
	
    os.remove("frames.zip")


    # create the chunk
    args = [
        "frames.zip", 
        framedir  
    ]
    subprocess.run(
        ["zip", '-r'] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    # push the chunk to amazone S3
    s3.upload_file("frames.zip", bucket_name, "frames.zip")

    return ("frames.zip")


def pull(framedir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
 
    # pull chunk from amazone S3
    s3.download_file(bucket_name, framedir, framedir)
    
	# unzip the chunk
    args = [
        framedir,
		"-d",
        "./"  
    ]
    subprocess.run(
        ["unzip"] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT	
    )

    return ("frames")


def draw(ref):

	files  = ref.keys()

	for file in files:
		path = os.path.join("frames", file)
		frame = cv2.imread(path)
		cv2.rectangle(frame,  (ref[file][0][0], ref[file][0][1]) ,  (ref[file][1][0], ref[file][1][1]) , (0, 255, 0), 2)
		cv2.imwrite(path, frame)

    
	return("Ok")


def main(args):
    
	key = args.get("key")
	access = args.get("access")
    
	ref = args.get("ref")
    
	framedir = pull("frames.zip", key, access)
    
	response = draw(ref)

	response = push('frames', key, access)


	
	return {"body": response}
