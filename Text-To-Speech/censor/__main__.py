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
    wav_file = wave.open("speeech.wav", 'rb')  
    nframes = wav_file.getnframes()
    frames = wav_file.readframes(nframes)
    # Convert audio frames to numpy array
    samples = np.frombuffer(frames, dtype=np.int16)
    samples = samples.copy()

    pull("index.json", ipv4)
    with open("index.json", 'r') as f:
        indexes = json.load(f)

    for index, s in enumerate(samples):
    
        for start, end in indexes:
            start_sample = int(start * len(samples))
            end_sample = int(end * len(samples))

            if index > start_sample and index < end_sample:
                samples[index] = 0
        
    # Convert the modified numpy array back to bytes
    new_frames = samples.tobytes()
    
    # Write the new frames to a new WAV file
    with wave.open("censor_speeech.wav", 'wb') as wav_out:
        wav_out.setparams(wav_file.getparams())
        wav_out.writeframes(new_frames)

    
    push("censor_speeech.wav", ipv4)


    return {"result" : "Ok"}