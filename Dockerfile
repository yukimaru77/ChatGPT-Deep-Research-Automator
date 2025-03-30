FROM python:3.10-alpine

RUN pip install --upgrade pip

EXPOSE 5900

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
COPY ./scripts /scripts

# Install temporary dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache --virtual .build-deps \
    alpine-sdk \
    curl \
    wget \
    unzip \
    gnupg 

# Install dependencies (Xvfb, x11vnc, fluxbox など)
RUN apk add --no-cache \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    bzip2-dev \
    readline-dev \
    sqlite-dev \
    git \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    chromium \
    tzdata \
    xclip

# Noto Sans
RUN curl -o /tmp/NotoSansCJKjp-hinted.zip https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip
RUN unzip -o -d /usr/share/fonts/noto /tmp/NotoSansCJKjp-hinted.zip

# Noto Serif
RUN curl -o /tmp/NotoSerifCJKjp-hinted.zip https://noto-website-2.storage.googleapis.com/pkgs/NotoSerifCJKjp-hinted.zip
RUN unzip -o -d /usr/share/fonts/noto /tmp/NotoSerifCJKjp-hinted.zip

# デフォルトだと root 以外がフォントを読めない
RUN chmod 644 /usr/share/fonts/noto/*.otf

# 後述の設定ファイル
COPY ./local.conf /etc/fonts/local.conf

# キャッシュ更新
RUN fc-cache -fv

# 確認
RUN fc-match "sans-serif"
RUN fc-match "serif"
ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=Asia/Tokyo


# Install x11vnc
RUN mkdir ~/.vnc
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

WORKDIR /app

RUN chmod -R +x /scripts

ENV PATH="/scripts:$PATH"
ENV DISPLAY=:0

# Delete temporary dependencies
RUN apk del .build-deps

CMD startup.sh
