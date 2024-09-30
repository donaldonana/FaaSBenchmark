FROM openwhisk/action-python-v3.9

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libavcodec-extra -y
 
RUN pip install python-swiftclient

RUN pip install gTTS

RUN pip install pydub>=0.23.1

RUN python3 -c "import pydub"
