#!/usr/bin/env python3

import os, shutil, argparse, yaml

groups = ['actions', 'animations', 'apps', 'categories', 'devices', 'emblems',
		  'emotes', 'filesystems', 'intl', 'mimetypes', 'places', 'status']

stockGroups = ['stock/chart', 'stock/code', 'stock/data', 'stock/form',
               'stock/image', 'stock/io', 'stock/media', 'stock/navigation',
               'stock/net', 'stock/object', 'stock/table', 'stock/text']

def getGroup(path):
	# we should never get warnings, that means we forgot to plan on a group
	# being present
	if 'stock' in path:
		for s in stockGroups:
			if s in path:
				return s
		else:
			return 'stock'
	else:
		for g in groups:
			if g in path:
				return g
		else:
			print('WARNING: unknown group in root path: ' + path)

def compileIcons(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if f == 'meta':
				r, iconName = os.path.split(root)
				groupName = getGroup(root)
				
				data = yaml.safe_load(open(os.path.join(root, f)))

				targets = {t.split(',')[0]:l for t, l in data.items()}

				# loop through each size in meta
				for sizeName, links in targets.items():
					out = os.path.join(outpath, groupName, sizeName)
					outFile = os.path.join(out, iconName)
					os.makedirs(out, exist_ok=True)

					# decide what to copy/link here
					cp = os.path.join(root, sizeName + '.png')

					if os.path.exists(os.path.join(root, 'link')):
						linkFile = root + '/link'
						
						if not os.path.exists(linkFile):
							print(sizeName, groupName, iconName, 1)
							continue

						with open(linkFile, 'r') as ln:
							lnSrcPath = ln.readlines()[0].rstrip()

						# links can be formated either <name> or <group>/<name>
						# if the former, we assume the same group as the
						# directory in which the link file is placed
						lnGroupName, lnSrcName = os.path.split(lnSrcPath)

						if not lnGroupName:
							lnGroupName = groupName

						prefix = '../..' if lnGroupName in groups else '../../..'

						lnSrc = os.path.join(prefix, lnGroupName, sizeName, lnSrcName)
						os.symlink(lnSrc, outFile)
							
					elif os.path.exists(os.path.join(root, 'icon')):
						if not os.path.exists(root + '/icon'):
							print(sizeName, groupName, iconName, 2)
							continue

						shutil.copy(root + '/icon', outFile)
							
					else:
						cp = os.path.join(root, sizeName + '.png')

						if not os.path.exists(cp):
							print(sizeName, groupName, iconName, 3)
							continue
						
						shutil.copy(cp, outFile)

					# now take care of all links in meta
					for ln in links:
						r, lnName = os.path.split(ln)
						r, lnSize = os.path.split(r)
						lnGroup = getGroup(ln)

						# TODO: doesn't correctly link stock
						prefix = '../..' if lnGroup in groups else '../../..'

						lnDir = os.path.join(outpath, lnGroup, lnSize)
						os.makedirs(lnDir, exist_ok=True)

						lnSrc = os.path.join(prefix, groupName, sizeName, iconName)
						os.symlink(lnSrc, os.path.join(lnDir, lnName))

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--input-directory', default='./', nargs=1)
parser.add_argument('-o', '--output-directory', default='icon_theme')
parser.add_argument('-q', '--quiet', action='store_true')

args = parser.parse_args()

rootpath = os.path.abspath(args.input_directory)
outpath = os.path.abspath(args.output_directory)

if os.path.exists(outpath):
	print(outpath + ' already exists. EXITING')
	exit()
	
for group in groups:
	compileIcons(os.path.join(rootpath, group))
	
for group in stockGroups:
	compileIcons(os.path.join(rootpath, group))

# copy index.theme
shutil.copy(os.path.join(rootpath, 'index.theme'), outpath)
