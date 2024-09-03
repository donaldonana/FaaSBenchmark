import subprocess
import os
import boto3


def push(chunkdir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
    # create the chunk
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
   

def decode(video, start, duration, chunkdir):
     
    # ensure the output directory exists
    os.makedirs(chunkdir, exist_ok=True)
    # decode 
    args = [
        "-i",  video, 
        "-ss", start, 
        "-t",  duration,
        '-vf', 'fps=4',
        os.path.join(chunkdir, 'frame_%04d.png')  
    ]
    subprocess.run(
        ["ffmpeg", '-y'] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
	
    return ("Ok")


def main(args):

    key = args.get("key")

    access = args.get("access")
    
    start = args.get("start", "6")   # start decoding  at n seconds

    duration = args.get("duration", "6")  # decode n seconds of video 

    chunkdir = args.get("chunkdir", "chunkdir") # path to the decode result (frames dicrectory)

    video = os.path.join("/app", 'queen.mp4')  # pull to amazone

    decode(video, str(start), str(duration), chunkdir)  
    
    push(chunkdir, key, access) 
	
    return {
        "status" : "Ok",
        "chunkdir": chunkdir,    
        "key" : args.get("key"),
        "access" : args.get("access")
    }
