#!/bin/bash
find -name '*.mkv' -exec mkvpropedit {} --set "title=" \;
