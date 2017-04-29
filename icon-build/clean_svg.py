#! /bin/python

import os, sys, shutil

path = os.path.abspath(sys.argv[1])

for root, dirs, files in os.walk(path):
	if root != path:
		rootname, ext = os.path.splitext(root)
		if ext == '.png':
			svgpath = rootname + '.svg'
			if os.path.exists(svgpath):
				with open(svgpath + '/meta', 'r') as f:
					newlines = f.readlines()

				with open(root + '/meta', 'a') as f:
					f.writelines([i.replace('.svg', '.png') for i in newlines])

				shutil.rmtree(svgpath)
