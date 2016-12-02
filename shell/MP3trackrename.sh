#!/bin/bash
for i in *.mp3
do
	TITLE="$(mediainfo "$i" | awk -F ': ' '/Track name/ {print $2;exit}' | tr -dc '[:alnum:]\ \(\)-')"
	mv "$i" "$TITLE.mp3"
done
