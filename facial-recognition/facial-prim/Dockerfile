FROM openwhisk/action-python-v3.9

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 cmake  -y

RUN python3 -m pip install opencv-Python

RUN pip install face_recognition

# RUN pip install boto3

RUN pip install python-swiftclient

COPY ./queen.png /app

 
