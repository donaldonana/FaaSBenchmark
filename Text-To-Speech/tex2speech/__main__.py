from io import BytesIO
from gtts import gTTS
import swiftclient
import datetime


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
 

def main(args):
    
    
    message = "What a load of bullshit! You can't even get the simplest thing right."

    ipv4 = args.get("ipv4", "192.168.1.120")
     
    tts = gTTS(text=message, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    result = mp3_fp.getvalue()
    
    with open("speeech.mp3", "wb") as f:
            f.write(result)

    push("speeech.mp3", ipv4)
    
    return {
         "MessageSize" : str(len(message)),
         "FileSize" : str(len(message))
         }
    

