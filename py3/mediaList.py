#!/usr/bin/python3
# mediaList.py - walk directory and list media

import os, sys, shutil

if os.path.exists(sys.argv[1]): 
	for folderNames, subFolders, fileNames in os.walk(sys.argv[1]):
		#print('The current folder is ' + folderNames)
		#for subFolder in subFolders:
			#print('Subfolder of ' + folderNames + ': ' + subFolder)
		for fileName in fileNames:
			if fileName.endswith('.mkv'):
				print('File inside ' + folderNames + ': ' + fileName)
		#print('')
	
else:
	print('Need a valid path to traverse')
