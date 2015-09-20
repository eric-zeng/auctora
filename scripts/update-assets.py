#! /usr/bin/env python

import glob
import os
import shutil
from subprocess import call

# This script copies asset files fetched from bower into another directory,
# so that it can be checked into git and served to users.
# Update and run this file whenever you add new packages from bower.

# Get the directory of this script regardless of where it is called from.
this_dir = os.path.dirname(os.path.realpath(__file__))

def copy_from_bower(sources, destination):
	"""
	Copies the files from bower_components to the specified location.
	Arguments:
		sources - a list of file paths, relative to the bower_components folder.
		destination - the file path of the destination folder, relative to the root.
	"""
	bower_path = os.path.join(this_dir, '../bower_components')

	full_dst = os.path.abspath(os.path.join(os.path.join(this_dir, '..'), destination))

	if not os.path.exists(full_dst):
		os.makedirs(full_dst)

	for src in sources:
		full_src = os.path.abspath(os.path.join(bower_path, src))
		print('Copying ' + full_src + ' to ' + full_dst + '/' + os.path.basename(src))
		shutil.copy2(full_src, full_dst)

# Fetch packages from bower
call(['bower', 'install'])

# JavaScript files to be copied over
js_dest_path = 'lib/js'
js_assets = [
	'bootstrap/dist/js/bootstrap.min.js',
	'jquery/dist/jquery.min.js',
	'typeahead.js/dist/typeahead.bundle.min.js'
]

# CSS Files to be copied over
css_dest_path = 'lib/css'
css_assets = [
	'bootstrap/dist/css/bootstrap.min.css',
	'bootstrap/dist/css/bootstrap-theme.min.css'
]

font_dest_path = 'lib/fonts'
font_assets = [
	'bootstrap/dist/fonts/glyphicons-halflings-regular.eot',
	'bootstrap/dist/fonts/glyphicons-halflings-regular.svg',
	'bootstrap/dist/fonts/glyphicons-halflings-regular.ttf',
	'bootstrap/dist/fonts/glyphicons-halflings-regular.woff',
	'bootstrap/dist/fonts/glyphicons-halflings-regular.woff2'
]

copy_from_bower(js_assets, js_dest_path)
copy_from_bower(css_assets, css_dest_path)
copy_from_bower(font_assets, font_dest_path)
