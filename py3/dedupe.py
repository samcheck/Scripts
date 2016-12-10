import os
import sys

import hashSHA1

def find_dupe(folder):
    dupes = {}
    for root, subdir, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root, filename)
            f_hash = hashSHA1.hashSHA1(path)
            if f_hash in dupes:
                dupes[f_hash].append(path)
            else:
                dupes[f_hash] = [path]
    return dupes

def join_dicts(dict_1, dict_2):
    for key in dict_2.keys():
        if key in dict_1:
            dict_1[key] = dict_1[key] + dict_2[key]
        else:
            dict_1[key] = dict_2[key]

def print_dupes(dict_1):
    results = list(filter(lambda x: len(x) > 1, dict_1.values()))
    if len(results) > 0:
        print('Dupes:')
        for result in results:
            print('='*80)
            for subresult in result:
                print('{}'.format(subresult))
    else:
        print('No dupes')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dupes = {}
        folders = sys.argv[1:]
        for i in folders:
            if os.path.exists(i):
                join_dicts(dupes, find_dupe(i))
        print_dupes(dupes)
