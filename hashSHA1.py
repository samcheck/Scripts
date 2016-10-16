#!/usr/bin/python3
# hashSHA1.py - hash SHA-1 of a given file and print
# Usage:import hashSHA1
#       hashSHA1.hashSHA1(<file>) - returns SHA1 hash of file

import hashlib, os

BLOCKSIZE = 65536 # set BLOCKSIZE for large files

def hashSHA1(in_file):
    ''' hashSHA1(<input file>) - takes a file (or path to file)
        returns the hex digest of the input'''
    if os.path.isfile(in_file): # Check if input is a file and hash
        sha1 =  hashlib.sha1()
        with open(in_file, 'rb') as file_to_hash:
            hash_buffer = file_to_hash.read(BLOCKSIZE)
            while len(hash_buffer) > 0:
                sha1.update(hash_buffer)
                hash_buffer = file_to_hash.read(BLOCKSIZE)
        return(sha1.hexdigest())
