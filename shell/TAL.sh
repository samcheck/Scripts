#!/bin/bash
# Credit to commentor Bee Lurgen
# https://www.quora.com/How-can-I-download-all-the-This-American-Life-podcasts-through-iTunes

STARTTIME=$(date +%s)

i=$1

#Base directories
out="Dl"
tmp="$out/tmp"
mp3Base="http://audio.thisamericanlife.org"
streamBase="http://stream.thisamericanlife.org"

##Temp files
rawMan="$tmp/${i}rawMan.txt"
localMan="$tmp/${i}localMan.txt"
localManForFFMPEG="$tmp/${i}localManForFFMPEG.txt"
remoteMan="$tmp/${i}remoteMan.txt"

tmpFiles=($rawMan $localMan $localManForFFMPEG $remoteMan)

##Final output
outFile="$out/#$i.mp3"

if [[ -z "$i" ]] ; then
  echo "ERROR: No episode number specified"
  exit 1
else
  if ! [[ $i =~ ^[1-9][0-9]*$ ]] ; then
      echo "ERROR: Not a valid number"
      exit 1
  fi
  if [[ $i -lt 544 ]] ; then
    wget -O "$outFile" "$mp3Base/$i.mp3"
  else
    mkdir -p "$tmp"
    stream="$streamBase/$i/stream"
    echo wget -O "$rawMan" "$stream/${i}_64k.m3u8" 2> /dev/null
    wget -O "$rawMan" "$stream/${i}_64k.m3u8" 2> /dev/null
    if [[ $? -ne 0 ]] ; then
      echo "ERROR: Stream manifest not found"
      exit 1
    fi
    cat "$rawMan" | grep '\.ts' | awk '{print var $0}' var="$stream/" > "$remoteMan"
    cat "$rawMan" | grep '\.ts' | awk '{print var $0}' var="file " >"$localManForFFMPEG"
    cat "$rawMan" | grep '\.ts' | awk '{print var $0}' var="$tmp/" > "$localMan"
    echo "Downloading parts..."
    wget -i "$remoteMan" -P "$tmp" 2>/dev/null
    echo "Concatenating..."
    ffmpeg -f concat -i "$localManForFFMPEG"  -b:a 64K -vn "$outFile" 2>/dev/null
    ENDTIME=$(date +%s)
    TOTALTIME=$(($ENDTIME - $STARTTIME))
    if [[ $? -eq 0 ]] ; then
      echo "Completed successfully.. $TOTALTIME seconds"
      echo "Cleaning up.."
      xargs rm < "$localMan"
      rm ${tmpFiles[*]}
    fi
  fi
fi
