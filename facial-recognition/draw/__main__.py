import subprocess
import os
import cv2
import numpy as np
import shutil
import boto3
import datetime



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
    
    key = args.get("key")
    
    access = args.get("access")
    
    ref = args.get("ref")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, key, access)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    draw(ref, chunkdir)
    process_end = datetime.datetime.now()

    push_begin = datetime.datetime.now()
    push(chunkdir, key, access)
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
        "key" : args.get("key"),
        "access" : args.get("access")
    }
