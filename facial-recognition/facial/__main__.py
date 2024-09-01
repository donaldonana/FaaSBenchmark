import os
import cv2
import boto3
import subprocess
import face_recognition



def pull(chunkdir, key, access):

    chunkdir = chunkdir + ".zip"

    # connexion to Remote Storage
    bucket_name = 'donaldbucket'
    s3 = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=access)
 
    # pull chunk from amazone S3
    s3.download_file(bucket_name, chunkdir, "/app/" + chunkdir)
    
	# unzip the chunk
    args = [
        "/app/" + chunkdir,
		"-d",
        "/app/"  
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


def facialRec(scenes, chunkdir, known_face_encodings):

	result = []

	chunkdir = "/app/"+chunkdir

	for scene in scenes :

		find = False
		box = []

		for file in scene["frames"] :

			path = os.path.join(chunkdir, file)

			frame = cv2.imread(path)

			rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			face_locations = face_recognition.face_locations(rgb_frame)
			face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

			for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			
				if matches[0] == True:

					find = True
					box = [(left, top), (right, bottom)]
					break

			if find:
				break

		scene["box"] = box
		scene["face"] = find
		result.append(scene)


	return result
		
     

def main(args):

    # amazone key         
	key = args.get("key")
	access = args.get("access")

	chunkdir = args.get("chunkdir", "chunkdir")

	video = os.path.join("/app", 'queen.png')  #toparam

	ref = args.get("ref")

	pull(chunkdir, key, access)

	refimg = matchFace(video)

	result = facialRec(ref, chunkdir, refimg)

	ref = {"scenes" : True, "frames" : result}

	return {
		"status" : "Ok",
		"ref" : ref,
        "chunkdir": chunkdir ,   # "chunkdir" toparam
		"key" : args.get("key"),
        "access" : args.get("access"),
	}
