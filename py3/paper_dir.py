#!/usr/bin/python3
# paper_dir.py - walk a given directory and 'clone' it to a new location with
# empty files

import sys
import os
import shutil
import logging
import errno

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def list_all(in_path):
    if os.path.exists(in_path) and os.path.isdir(in_path):
        for root, dirs, files in os.walk(in_path):
            for filename in files:
                yield root, dirs, filename

def clone(in_path, new_path):
    names = os.listdir(in_path)
    os.makedirs(new_path)
    for name in names:
        in_path_name = os.path.join(in_path, name)
        new_path_name = os.path.join(new_path, name)
        if os.path.isdir(in_path_name):
            clone(in_path_name, new_path_name)
        else:
            touch(new_path_name)


def touch(path_file):
    try:
        # open file in append mode in case it exists, then write an empty string
        with open(path_file, "a") as f:
            f.write("")
    except os.error:
        # create the directory, if it does not exist
        os.makedirs(os.path.dirname(path_file))
        with open(path_file, "a") as f:
            f.write("")

def main():
    in_path = sys.argv[1] # take args in from commandline
    new_path = sys.argv[2]
    clone(in_path, new_path)

if __name__ == "__main__":
    main()
