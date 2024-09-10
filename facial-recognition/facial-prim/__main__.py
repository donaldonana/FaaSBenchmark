import os
import cv2
import subprocess
import face_recognition
import datetime
import swiftclient



def pull(chunkdir, ipv4):

	chunkdir = chunkdir + ".zip"

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
	obj = conn.get_object(container, chunkdir)
	with open(chunkdir, 'wb') as f:
		f.write(obj[1])

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


def matchFace(imgref):
	# Match face list
	known_face_encodings = []
	# load the reference image from S3
	image = face_recognition.load_image_file(imgref)
	# encode all face in ref. imagethere is normally only one
	known_face_encodings.append(face_recognition.face_encodings(image).pop(0))

	return known_face_encodings

  

def facialRecPrime(scenes, chunkdir, known_face_encodings):

	result = {}
	chunkdir = chunkdir

	if scenes:
		for scene in scenes :

			for file in scene["frames"] :
				path = os.path.join(chunkdir, file)
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
	
	else:
		files = sorted([f for f in os.listdir(chunkdir) if f.endswith('.webp')])
		for file in files:
            
			path = os.path.join(chunkdir, file)
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
	ipv4 = args.get("ipv4", "192.168.1.120")

	chunkdir = args.get("chunkdir", "chunkdir")

	imgref = os.path.join("/app", 'queen.png')  #toparam

	ref = args.get("ref", None)

	pull_begin = datetime.datetime.now()
	pull(chunkdir, ipv4)
	pull_end = datetime.datetime.now()

	process_begin = datetime.datetime.now()
	refimg = matchFace(imgref)
	result = facialRecPrime(ref, chunkdir, refimg)
	process_end = datetime.datetime.now()


	ref = {"scene" : False, "scenes" : result}

	times = args.get("times")
	
	times["facerecprim"] = {
        "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
        "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1)
    }

	return {
		"status" : "Ok",
		"ref" : ref,
        "times" : times,
        "chunkdir": chunkdir ,   # "chunkdir" toparam
		"ipv4" : ipv4
	}
