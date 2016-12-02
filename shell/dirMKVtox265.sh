#!/bin/bash


find -name '*.mkv' -exec ffmpeg -i {} -c:v libx265 -preset medium -x265-params crf=28 -c:a aac -strict experimental -b:a 128k {}_x265.mkv \;
