import subprocess
import os
import cv2
import numpy as np
import shutil
import boto3


def push(chunkdir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)

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
 
    # push the chunk to amazone S3
    s3.upload_file(chunkdir + ".zip", bucket_name, chunkdir + ".zip")

    return ("Ok")


def pull(chunkdir, key, access):

    chunkdir = chunkdir + ".zip"

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
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
 

def draw(ref, chunkdir):

    os.makedirs("newchunkdir", exist_ok=True)

    if ref["scene"]:
        for scene in ref["scenes"]:

            if scene["face"]:
                box = scene["box"]

                for file in scene["frames"]:
                    path = os.path.join(chunkdir, file)
                    newpath = os.path.join("newchunkdir", file)
                    frame = cv2.imread(path)
                    cv2.rectangle(frame,  (box[0][0], box[0][1]) ,  (box[1][0], box[1][1]) , (0, 255, 0), 2)
                    cv2.imwrite(newpath, frame)

    else:
        files  = ref["scenes"].keys()

        for file in files:
            path = os.path.join(chunkdir, file)
            newpath = os.path.join("newchunkdir", file)
            frame = cv2.imread(path)
            box = ref["scenes"][file]
            cv2.rectangle(frame,  (box[0][0], box[0][1]) ,  (box[1][0], box[1][1]) , (0, 255, 0), 2)
            cv2.imwrite(newpath, frame)

    shutil.rmtree(chunkdir)
    shutil.move("newchunkdir", chunkdir)

    return("Ok")


def main(args):
    
    key = args.get("key")
    
    access = args.get("access")
    
    ref = args.get("ref")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull(chunkdir, key, access)
    
    draw(ref, chunkdir)
    
    push(chunkdir, key, access)
    
    return {
        "status" : "Ok",
        "ref" : ref,
        "chunkdir": chunkdir,   
        "key" : args.get("key"),
        "access" : args.get("access")
    }
