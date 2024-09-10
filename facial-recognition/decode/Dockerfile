FROM openwhisk/action-python-v3.9

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y 

# RUN pip install boto3
 
COPY ./queen.mp4 /app

COPY ./nature.mp4 /app

RUN pip install python-swiftclient
