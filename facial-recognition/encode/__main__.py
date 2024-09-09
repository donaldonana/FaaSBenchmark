import subprocess
import os
import boto3
import re
import datetime



def push(chunkdir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
 
    # push the chunk to amazone S3
    s3.upload_file(chunkdir + ".mp4", bucket_name, chunkdir + ".mp4")

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


def encode(chunkdir):

    files = os.listdir('.')   
    pattern = r'frame_(\d+)\.webp'  
    # Extract numbers from filenames that match the pattern
    numbers = [int(re.search(pattern, f).group(1)) for f in files if re.search(pattern, f)]

    if numbers:
        start_number = min(numbers) 
        result = chunkdir+".mp4" 
        chunkdir = chunkdir+"/frame_%004d.webp"
        args = [
            "-framerate",  "2", 
            "-start_number", str(start_number), 
            "-i", chunkdir, 
            "-c:v",  "libx264",
            '-t', '6',
            '-pix_fmt', "yuv420p",
            result,
        ]

        process =  subprocess.run(
            ["ffmpeg", '-y'] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        return (True)
    
    else:
        return False



def main(args):

    key = args.get("key")
    
    access = args.get("access")
    
    chunkdir = args.get("chunkdir", "chunkdir")
    
    pull_begin = datetime.datetime.now()
    pull(chunkdir, key, access)
    pull_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    response = encode(chunkdir)
    process_end = datetime.datetime.now()

    if response:
        push_begin = datetime.datetime.now()
        push(chunkdir, key, access)
        push_end = datetime.datetime.now()
        push_time = (push_end - push_begin) / datetime.timedelta(seconds=1)
    else: 
        push_time = 0


    times = args.get("times")

    times["encode"] = {
        "push" : push_time,
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
    }
    
    return {
        "status" : "Ok",
        "times" : times,
    }



# ffmpeg -y -framerate 4 -i frame_%004d.png -c:v libx264 -r 8 -pix_fmt yuv420p output.mp4
