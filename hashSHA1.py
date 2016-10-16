#!/usr/bin/python3
# hashSHA1.py - hash SHA-1 of a given file and print
# Usage: hashSHA1.py <file>

import hashlib, os

BLOCKSIZE = 65536 # set BLOCKSIZE for large files

def hashSHA1(in_file):
    if os.path.isfile(in_file):
        sha1 =  hashlib.sha1()
        with open(in_file, 'rb') as file_to_hash:
            hash_buffer = file_to_hash.read(BLOCKSIZE)
            while len(hash_buffer) > 0:
                sha1.update(hash_buffer)
                hash_buffer = file_to_hash.read(BLOCKSIZE)
        return(sha1.hexdigest())
