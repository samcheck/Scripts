#!/bin/bash
# ----------------------------------------------------------------------------
# https://superuser.com/questions/650848/realtime-transcoding-to-h264aac-in-matroska-container
# This script is a helper to transcode a video to H264+AAC with subtitles to a
# Matroska (.mkv) container that is suitable for live streaming to a mobile
# device. It will transcode media that is not H264 or that has too high
# resolution. It will not upsample content.
#
# Other suitable containers (and reasons for not using them) include:
# * ASF (Microsoft, proprietary)
# * MPEG2 Transport Stream (Standard, only supports bitmap subtitles)
# * WebM (Has no support for metadata)
# * DivX (Can't contain H264)
# * FLV (Proprietary Bad support on target device)
# * MP4 (Only bitmap subtitles, didn't work for streaming with FFMPEG)
# * OGG (No support for H264)
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Video options
# ----------------------------------------------------------------------------
LINES=720

# One of: ultrafast,superfast, veryfast, faster, fast, medium, slow, slower,
# veryslow or placebo
PRESET=ultrafast

# One of: baseline, main, high, high10, high422 or high444
PROFILE=high10

# One of: film animation grain stillimage psnr ssim fastdecode zerolatency
TUNE=zerolatency

# ----------------------------------------------------------------------------
# Audio options
# ----------------------------------------------------------------------------
AUDIO="-c:a libfaac -b:a 128k -ar 48000 -ac 2 -async 1"

SUBTITLES="-c:s copy"

# ----------------------------------------------------------------------------
# Read input video parameters
# ----------------------------------------------------------------------------
IN_RESOLUTION=`/usr/bin/ffmpeg -i "${1}" 2>&1 | grep Video | \
    perl -lane 'print $1 if /(\d+x\d+)/'`
IN_CODEC=`/usr/bin/ffmpeg -i "${1}" 2>&1 | grep Video | \
    perl -lane 'print $1 if /Video: (\S+)/'`
IN_DIMS=(${IN_RESOLUTION//x/ })
V_TRANSCODE="-c:v libx264 -bsf:v h264_mp4toannexb -preset ${PRESET} \
    tune ${TUNE} -profile:v ${PROFILE}"
V_COPY="-c:v copy -bsf:v h264_mp4toannexb"

if [ "${IN_DIMS[1]}" > "${LINES}" ]; then
    SCALE="-filter:v scale=-1:${LINES} ${OPT_TRANSCODE}"
else
    if ["${IN_CODEC}" != "h264" ]; then
        VIDEO=$OPT_TRANSCODE
    else
        VIDEO=$V_COPY
    fi
fi

exec /usr/bin/ffmpeg -threads `nproc` -i "${1}" $VIDEO $AUDIO $SUBTITLES \
    -f matroska -y "${2}" &> /store/tmp/log
