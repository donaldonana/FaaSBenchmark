import subprocess
import os
import cv2
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
    
    key = args.get("key")
    
    access = args.get("access")
    
    ref = args.get("ref")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, key, access)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    keep(ref, chunkdir)
    process_end = datetime.datetime.now()

    push_begin = datetime.datetime.now()
    push(chunkdir, key, access)
    push_end = datetime.datetime.now()


    times = ref = args.get("times")

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
        "key" : args.get("key"),
        "access" : args.get("access")
    }
