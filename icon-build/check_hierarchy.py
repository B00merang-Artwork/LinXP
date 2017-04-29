#! /bin/python

import os, sys, yaml, argparse

groups = ['actions', 'animations', 'apps', 'categories', 'devices', 'emblems',
		  'emotes', 'filesystems', 'intl', 'mimetypes', 'places', 'status']

stockGroups = ['stock/chart', 'stock/code', 'stock/data', 'stock/form',
               'stock/image', 'stock/io', 'stock/media', 'stock/navigation',
               'stock/net', 'stock/object', 'stock/table', 'stock/text']

def inspectGroup(path):
	for root, dirs, files in os.walk(path):
		for f in files:
			if f == 'link':
				with open(os.path.join(root, f), 'r') as of:
					linkpath = of.readlines()[0].rstrip()
				if not os.path.exists(os.path.join(path,linkpath)):
					print('WARNING: link {} points to an invalid directory'.format(linkpath))
					
			elif f == 'icon':
				if os.path.splitext(root)[1] == '.icon':
					continue
				else:
					print('WARNING: icon detected in non-icon folder ' + root)
					
			elif f == 'meta':
				data = yaml.safe_load(open(os.path.join(root, f)))

				# no need to check meta if there is an icon or link present
				if os.path.exists(os.path.join(root, 'link')) or os.path.exists(os.path.join(root, 'icon')):
					continue
				else:
					#otherwise check to see that we have the right images
					for t in data:
						size = t.split(',')[0]
						extension = os.path.splitext(root)[1]
						name = size + extension
						if os.path.exists(os.path.join(root, name)):
							continue
						else:
							if not args.quiet:
								print('WARNING: icon {} not found in {}'.format(name, root))
				
parser = argparse.ArgumentParser()

parser.add_argument('-f', '--input-directory', default='./', nargs=1)
parser.add_argument('-q', '--quiet', action='store_true')

args = parser.parse_args()

rootpath = os.path.abspath(args.input_directory[0])

for group in groups:
	inspectGroup(os.path.join(rootpath, group))
	
for group in stockGroups:
	inspectGroup(os.path.join(rootpath, group))
