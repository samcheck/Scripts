#!/usr/bin/python3
# paper_dir.py - walk a given directory and 'clone' it to a new location with
# empty files

import sys
import os
import shutil
import logging
import errno
import argparse



def clone(in_path, new_path):
    names = os.listdir(in_path)
    if not os.path.exists(new_path): #create the path if it doesn't exist
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
    # set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input directory to clone.')
    parser.add_argument('-o', '--output', help='Directory to clone into.')
    args = parser.parse_args()
    if args.input and args.out:
        clone(args.input, args.out)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
