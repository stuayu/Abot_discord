FROM python:3.10.0-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install locales -y && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN apt-get install -y \
    wget \
    xz-utils \
    git

RUN cd /tmp && \
    wget https://github.com/yt-dlp/FFmpeg-Builds/releases/download/autobuild-2021-10-31-12-47/ffmpeg-n4.4.1-1-g0de5c9e2e4-linux64-gpl-4.4.tar.xz && \
    tar Jxvf ./ffmpeg-n4.4.1-1-g0de5c9e2e4-linux64-gpl-4.4.tar.xz && \
    cp ./ffmpeg*/bin/ffmpeg /usr/local/bin/ && \
    cp ./ffmpeg*/bin/ffplay /usr/local/bin/ && \
    cp ./ffmpeg*/bin/ffprobe /usr/local/bin/ 

RUN pip install --upgrade pip && \
    pip install discord.py[voice] \
    bs4 \
    requests \ 
    speedtest-cli
RUN python3 -m pip install --upgrade git+https://github.com/yt-dlp/yt-dlp

ADD /src /app/

CMD [ "python3","main.py" ]
