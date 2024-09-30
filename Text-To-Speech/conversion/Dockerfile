FROM openwhisk/action-python-v3.10

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libavcodec-extra -y 
 
RUN pip install python-swiftclient

RUN pip install pydub>=0.23.1