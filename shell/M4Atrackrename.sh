#!/bin/bash
for i in *.m4a
do
	TITLE="$(mediainfo "$i" | awk -F ': ' '/Track name/ {print $2;exit}' | tr -dc '[:alnum:]\ \(\)-')"
	ARTIST="$(mediainfo "$i" | awk -F ': ' '/Performer/ {print $2;exit}' | tr -dc '[:alnum:]\ \(\)-')"
	mv "$i" "$ARTIST - ${TITLE%.m4a}.m4a"
done
