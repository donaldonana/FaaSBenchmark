from pydub import AudioSegment
from io import BytesIO
import os
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

    obj = conn.get_object(container, obj)
    with open(obj, 'wb') as f:
        f.write(obj[1])
 

    return ("Ok")


def main(args):

    ipv4 = args.get("ipv4", "192.168.1.120")

    # pull("speeech.mp3", ipv4)
    
    # mp3file =  open("speeech.mp3", "rb").read()
    # input = BytesIO(mp3file)
    # speech = AudioSegment.from_mp3(input)
    # inputSize = len(input.getvalue())
    # output = BytesIO()
    # speech.export(output, format="wav")
    # result = output.getvalue()
    
    # with open("speeech.wav", "wb") as f:
    #         f.write(result)
    
    return {
         "Outputfilesize" : "str(len(output.getvalue()))"
         }
    

