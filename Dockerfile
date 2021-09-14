FROM python:3.9.6-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y \
    wget \
    xz-utils
ENV TZ='Asia/Tokyo'
RUN wget https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-09-09-12-23/ffmpeg-n4.4-150-gb5cdf08cae-linux64-gpl-4.4.tar.xz && \
    tar Jxvf ./ffmpeg-n4.4-150-gb5cdf08cae-linux64-gpl-4.4.tar.xz && \
    cp ./ffmpeg*/bin/ffmpeg /usr/local/bin/ && \
    cp ./ffmpeg*/bin/ffplay /usr/local/bin/ && \
    cp ./ffmpeg*/bin/ffprobe /usr/local/bin/ 

RUN pip install --upgrade pip && \
    pip install discord.py[voice] \
    bs4 \
    requests \ 
    youtube-dl \
    speedtest-cli 

COPY /src /app/

CMD [ "python3","main.py" ]
