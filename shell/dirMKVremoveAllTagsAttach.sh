#!/bin/bash
find -name '*.mkv' -exec mkvpropedit {} --set "title=" --edit track:v1 --set name= --edit track:a1 --set name= --tags all: --delete-attachment mime-type:image/jpeg \;
