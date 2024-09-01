import os
import cv2
import boto3
import subprocess
import face_recognition



def pull(framedir, key, access):

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
 
    # pull chunk from amazone S3
    s3.download_file(bucket_name, framedir, "/app/" + framedir)
    
	# unzip the chunk
    args = [
        "/app/" + framedir,
		"-d",
        "/app/"  
    ]
    subprocess.run(
        ["unzip"] + args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    return ("/app/frames")


def matchFace(imgref):
	# Match face list
	known_face_encodings = []
	# load the reference image from S3
	image = face_recognition.load_image_file(imgref)
	# encode all face in ref. imagethere is normally only one
	known_face_encodings.append(face_recognition.face_encodings(image).pop(0))

	return known_face_encodings

     
def facialRecPrime(framedir, known_face_encodings):
      
	result = {}
      
	files = sorted([f for f in os.listdir(framedir) if f.endswith('.png')])
    
	for file in files:
            
		path = os.path.join(framedir, file)
		frame = cv2.imread(path)
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		face_locations = face_recognition.face_locations(rgb_frame)
		face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

		for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                  
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                  
			if matches[0] == True:
				box = [(left, top), (right, bottom)]
				result[str(file)] = box

	return result
       


def main(args):

    # amazone key         
	key = args.get("key")
	access = args.get("access")

	video = os.path.join("/app", 'queen.png') 

	framedir = pull("frames.zip", key, access)

	refimg = matchFace(video)

	result = facialRecPrime(framedir, refimg)

	return ({
		"ref" : result,
		"key" : args.get("key"),
        "access" : args.get("access")
	})
