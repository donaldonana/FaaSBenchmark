import swiftclient
import subprocess
import os
import json
import wave
import numpy as np


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


def main(args):

    ipv4 = args.get("ipv4", "192.168.1.120")

    pull("speeech.wav", ipv4)
    
    with wave.open("speeech.wav", 'rb') as wav_file:
        params = wav_file.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]
        
        # # Read the audio frames
        frames = wav_file.readframes(n_frames)
        
        # # Convert audio frames to numpy array
        audio = np.frombuffer(frames, dtype=np.int16)

        audio = audio.copy() 


    pull("index.json", ipv4)
    with open("index.json", 'r') as f:
        indexes = json.load(f)

    
    for start, end in indexes:
        start_sample = int(start * framerate)
        end_sample = int(end * framerate)
        
        # Mute the audio samples by setting them to 0
        audio[start_sample:end_sample] = 0
    
    # Convert the modified numpy array back to bytes
    new_frames = audio.tobytes()
    
    # Write the new frames to a new WAV file
    with wave.open("speeech.wav", 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(new_frames)

    
    push("speeech.wav", ipv4)


    
    return {"result" : "Ok"}
    

