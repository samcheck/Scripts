#!/bin/bash
find -name '*.mkv' -exec mkvmerge -o {}-new.mkv --subtitle-tracks 1,2 {} \;
