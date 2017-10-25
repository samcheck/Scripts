#!/bin/bash
find -name '*.mkv' -exec mkvextract tracks {} 2:{}.srt \;
