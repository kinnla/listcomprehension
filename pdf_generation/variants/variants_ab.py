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
$ python3 variants_ab test_ab.tex

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
	parser.add_argument('-o', '--output', help='the output file name')
	return parser.parse_args()


def variants(tex_doc):
	""" Generates variants of a tex documents

	tex_doc -- the tex document as a string
	"""
	
	# for any of the three markers, create an iterator of its matches
	iter1 = re.finditer(r"\*A\*", tex_doc)
	iter2 = re.finditer(r"\*\*\*", tex_doc)
	iter3 = re.finditer(r"\*B\*", tex_doc)

	# now parallely iterate on all matches 
	index_of_last_match = -1
	while True:
		matches = (next(iter1, None), next(iter2, None), next(iter3, None))

		# if all iterators exhausted simultaneously: we are fine
		if matches == (None,)*3:
			break

		# if any iterator exhausted before the others: that's a problem
		assert not None in matches, "Inconsistent number of markers. Please check tex source."

		# check that indices are ascending
		assert index_of_last_match < matches[0].start(0), "New Variant started before old one ended"
		assert matches[0].start(0) < matches[1].start(0), "Variant stated with *** instead of *A*"
		assert matches[1].start(0) < matches[2].start(0), "Variant ended before ***"

	l= re.findall(r"\*\*\*", tex_doc)
	l=re.search(r"\*\*\*", tex_doc)
	l=[r for r in re.finditer(r"\*\*\*", tex_doc)]
	print(l)

	regex_a = re.compile(r"\*A\*(.*?)\*\*\*.*?\*B\*", re.DOTALL)
	regex_b = re.compile(r"\*A\*.*?\*\*\*(.*?)\*B\*", re.DOTALL)
	yield re.sub(regex_a, r'\1', tex_doc)
	yield re.sub(regex_b, r'\1', tex_doc)

def main():

	# parse command line arguments 
	args = parse_args()
	if not args.output:
		args.output = args.texfile.replace('.tex','.pdf')

	# read the tex doc
	with open(args.texfile, 'r') as file:
		tex = ''.join(file.readlines())

	# create PDF series
	util.create_pdf_series(tex, args, variants(tex))

	# open the combined pdf containing all variants
	os.system('open ' + args.output)

# execute only if run as a script
if __name__ == "__main__":
    main()

