from gtts import gTTS
# from pydub import AudioSegment
from io import BytesIO
import datetime
import swiftclient



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
    
    
    message = 'You’re doing a fantastic job! Keep up the great work.'
    message = 'You are such an idiot! This is a fucking mess, and you screwed everything up!'
    message = "I can't believe this shit happened again! You're a complete asshole!"
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
    

