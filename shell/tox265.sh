#!/bin/bash
if [ -n "$1" ]
then
ffmpeg -i "$1" -c:v libx265 -preset medium -x265-params crf=26 -c:a aac -strict experimental -b:a 196k "$1"x265.mkv
else
echo "Usage: `basename $0` input.file"
fi
