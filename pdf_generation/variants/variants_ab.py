#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This skript creates two variants of a tex file by and compiles them to a single pdf.
How to use:

1. edit you tex file and include variants
  - *A* marks the start of variant A
  - *** delimits variants A and B
  - *B* marks the end of variant B
  - example: *A*it's night time in Berlin***it's day time in Berlin*B*

2. Run the script
  - python3 variants_ab 

example:
>> python3 variants_ab test_ab.tex

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

# a symlink to lib is contained in the git repository
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

