import swiftclient
import subprocess
import os


def push(obj, ipv4):

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
 
    with open(obj, 'rb') as f:
        conn.put_object(container, obj, contents=f.read())
 
    return ("Ok")


def pull(obj, ipv4):
  
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

    file = conn.get_object(container, obj)
    with open("speeech.mp3", 'wb') as f:
        f.write(file[1])

    return ("Ok")


def main(args):

    ipv4 = args.get("ipv4", "192.168.1.120")

    pull("speeech.mp3", ipv4)
    
    args = [
            "-i", "speeech.mp3", 
            "speeech.wav",
        ]
    
    subprocess.run(
            ["ffmpeg", '-y'] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
    
    push("speeech.wav", ipv4)

    return {"Outputfilesize" : os.path.getsize("speeech.mp3")}
    

