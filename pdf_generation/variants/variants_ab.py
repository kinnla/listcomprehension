#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is a hybrid:
- a python script that produces variants of a tex doc and compiles them to a single pdf
- an embedded tex document with string markers

You can use it to produce unique versions of work sheets or tests. 
This file contains a fake math test as an example.

How to use:
1. Paste your tex doc below the script (### note the comment marker ###)
2. Insert markers to your tex doc that you want to replace
3. Define the dictionary replacements (top of the script)
4. Run the script

example:
>> python3 -m variants.variants_ab exam.tex

Prerequisits:
- latex
- python 3.x
- PyPDF2 python module
- tested on macOS
"""

import argparse
import os
import subprocess
import PyPDF2
import time
import shutil
import re
import sys

from lib import util

def parse_args():
	"""parse command line arguments and return them as Namespace"""

	parser = argparse.ArgumentParser(
		description='Generates variants from an embedded tex doc and compiles them to a combined PDF.')
	parser.add_argument('texfile', help='the tex file where the two variants shall be created for')
	parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
	return parser.parse_args()


def variants(tex_doc, args):
	""" Generates variants of a tex documents

	tex_doc -- the tex document as a string
	args -- the command line options as a Namespace object
	"""
	
	yield re.sub(r"\*A\*(.*?)\*\*\*.*?\*B\*", r'\1', tex_doc)
	yield re.sub(r"\*A\*.*?\*\*\*(.*?)\*B\*", r'\1', tex_doc)

def main():

	# parse command line arguments
	args = parse_args()

	# read the tex doc
	with open(args.texfile, 'r') as file:
		tex = ''.join(file.readlines())

	# create PDF series
	util.create_pdf_series(tex, args, variants(tex, args))

	# open the combined pdf containing all variants
	os.system('open ' + args.output)

# execute only if run as a script
if __name__ == "__main__":
    main()

