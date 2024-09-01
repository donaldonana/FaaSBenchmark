import subprocess
import os
import cv2
import shutil
import boto3


def push(framedir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)

    os.remove("frames.zip")

    # create the chunk
    args = [
        "frames.zip", 
        "frames"  
    ]
    subprocess.run(
        ["zip", '-r'] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    # s3.delete_object(Bucket=bucket_name, Key="frames.zip")
 
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

    return ("/app/frames")


def keep(ref):
    
    actual = [f for f in os.listdir("frames") if f.endswith('.png')]
    final  = ref.keys()

    for file in actual:
        if file not in final:
            path =  os.path.join("frames", file)
            os.remove(path)

    return("frames")


def main(args):
    
	key = args.get("key")
	access = args.get("access")
    
	ref = args.get("ref")
    
	framedir = pull("frames.zip", key, access)
    
	path =  keep(ref)

	response = push(path, key, access)
	
	return {"body": str(sorted([f for f in os.listdir(path)]))}
