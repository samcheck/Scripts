#! /bin/bash

# get all files that start with a number
for file in [0-9]* ; do
    # only process start start with a number
    # followed by one or more space characters
    if [[ $file =~ ^[0-9]+[[:blank:]]+(.+) ]] ; then
        # display original file name
        echo "< $file"
        # grab the rest of the filename from
        # the regex capture group
        newname="${BASH_REMATCH[1]}"
        echo "> $newname"
        # uncomment to move
        mv "$file" "$newname"
    fi
done
