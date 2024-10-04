from io import BytesIO
from gtts import gTTS
import swiftclient
import datetime
import os


def pull(obj, ipv4):
  
    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

    out = obj 

    # Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)
    container = 'whiskcontainer'

    file = conn.get_object(container, obj)
    with open(out, 'wb') as f:
        f.write(file[1])

    return ("Ok")


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


def toSpeech(file):

    with open(file, "r") as f:
            message = f.read()
     
    tts = gTTS(text=message, lang='en')
    mp3fp = BytesIO()
    tts.write_to_fp(mp3fp)
    result = mp3fp.getvalue()
    
    with open("speeech.mp3", "wb") as f:
            f.write(result)
    
    return "speeech.mp3", message
 

def main(args):
    
    ipv4 = args.get("ipv4", "192.168.1.120")

    pull_begin = datetime.datetime.now()
    pull("texte.txt", ipv4)
    pull_end = datetime.datetime.now()

    
    process_begin = datetime.datetime.now()
    result, message = toSpeech("texte.txt")
    process_end = datetime.datetime.now()

    push_begin = datetime.datetime.now()
    push(result, ipv4)
    push_end = datetime.datetime.now()

    response = {
         "MessageSize" : str(len(message)),
         "fileSize" : os.path.getsize(result),
         "text2speech" : {
            "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
            "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
            "push" : (push_end - push_begin) / datetime.timedelta(seconds=1)
         }
        }
    
    return  {"response" : response, "ipv4" : ipv4}
    

