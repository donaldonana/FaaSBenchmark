FROM openwhisk/action-python-v3.9

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y 
	
# RUN pip install boto3 

RUN python3 -m pip install opencv-Python

RUN pip install python-swiftclient