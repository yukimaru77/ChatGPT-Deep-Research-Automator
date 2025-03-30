#!/bin/sh

rm -f /tmp/.X0-lock

# Xvfb を起動
Xvfb :0 -screen 0 1280x720x16 &
sleep 3

# Fluxbox を起動
fluxbox -display :0 &
sleep 2

# x11vnc を起動
x11vnc -display :0 -forever -usepw &
sleep 2

# 少し待機
sleep 5

# コンテナを終了させずに待機状態にする
tail -f /dev/null
