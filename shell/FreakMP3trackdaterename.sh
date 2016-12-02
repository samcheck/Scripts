#!/bin/bash
# renames Freakonomics Tracks using mediainfo to get title and grabs date from exisitng filename
for i in *.mp3
do
	TITLE="$(mediainfo "$i" | awk -F ': ' '/Track name/ {print $2;exit}' | tr -dc '[:alnum:]\ \(\)-')"
	DATE="$(tr -dc '0-9' <<< $i | awk 'BEGIN {OFS="-"}{print substr($1,5,2), substr($1,1,2), substr($1,3,2)}')"
	mv "$i" "Freakonomics 20$DATE $TITLE.mp3"
done
