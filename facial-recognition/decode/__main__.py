import subprocess
import os
import datetime
import swiftclient



def pull(video, ipv4):

    # Swift identifiant
    auth_url = f'http://{ipv4}/auth/v1.0'
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
    
    obj_tuple = conn.get_object(container, video)
    with open(video, 'wb') as f:
        f.write(obj_tuple[1])


    # # connexion to Remote Storage
    # bucket_name = 'donaldbucket'
    # s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
    # # pull video from amazone
    # s3.download_file(bucket_name, video, video)


def push(chunkdir, ipv4):

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

    # Swift identifiant
    auth_url = f'http://{ipv4}/auth/v1.0'
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


    # # connexion to Remote Storage
    # bucket_name = 'donaldbucket'
    # s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
    
 
    # # push the chunk to amazone S3
    # s3.upload_file(chunkdir + ".zip", bucket_name, chunkdir + ".zip")

    return ("Ok")
   

def decode(video, start, duration, chunkdir):
     
    # ensure the output directory exists
    os.makedirs(chunkdir, exist_ok=True)
    # decode 
    args = [
        "-i",  video, 
        "-ss", start, 
        '-t', duration,      
        '-vf', 'fps=16',
        '-c:v', 'libwebp',              
        os.path.join(chunkdir, 'frame_%04d.webp')   
    ]
    subprocess.run(
        ["ffmpeg", '-y'] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
	
    return ("Ok")


def main(args):

    ipv4 = args.get("ipv4", "192.168.1.120:8080")

    # start decoding  at n seconds
    start = args.get("start", "6")
    # decode n seconds of video    
    duration = args.get("duration", "6")  

    # path to the decode result (frames dicrectory)
    chunkdir = args.get("chunkdir", "chunkdir") 

    schema = args.get("schema", "S1")

    video = args.get("video", "queen.mp4") 

    pull(video, ipv4)

    process_begin = datetime.datetime.now()
    decode(video, str(start), str(duration), chunkdir)
    process_end =  datetime.datetime.now()
    
    push_begin = datetime.datetime.now()
    push(chunkdir, ipv4)
    push_end = datetime.datetime.now()

    times = {

        "decode" : {
            "push" : (push_end - push_begin) / datetime.timedelta(seconds=1),
            "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        },

        "schema" : schema,
        "video" : video
    }

	
    return {
        "status" : "Ok",
        "chunkdir": chunkdir,    
        "key" : args.get("key"),
        "access" : args.get("access"),
        "times" : times
    }
