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
import csv
import locale

def variants(tex_doc, n=1):
  """ Generates variants of a tex documents

  tex_doc -- the tex document as a string
  n -- the number of variants to be generated (default 1)
  """

  # additional contents for the replacements dictionary
  B = ['-2', '-3', '-4', '+\\frac{1}{2}', '+\\frac{1}{3}', '+\\frac{2}{3}']
  C = ['+\\frac{1}{2}', '+\\frac{1}{3}', '+\\frac{2}{3}', '-\\frac{1}{3}', '-\\frac{2}{3}']

  # dictionary of replacements
  replacements = {
    '(NORMALFORM)': ['x^2' + b + 'x' + c for b in B for c in C],
    '(2A)': [a + "'(x)=" + b for a in 'fgh' for b in ['x^2', '\\sqrt{x}', 'x^3', '-2x', '\\frac{x}{3}']],
    '(2B)': [a + ',' + b + '\\overline{' + c + '}' for a in "01" for b in "789" for c in "23456"],
    '(2C)': [a + '\\in\\mathbb{' + b + '}' for a in "xyabcni" for b in "NRQZ"],
    '(2D)': [a + '\\neq-' + str(b) for a in "xyz" for b in range (1001, 1010)]
  }

  # loop n times
  for i in range(n):

    # create a variant of the tex document
    # don't need to clone here, as replace will generate a copy
    variant = tex_doc

    # iterate on the replacement keys
    for key in replacements:

      # determine the actual replacement, then replace
      l = replacements[key]
      replacement = l[i % len(l)]
      variant = variant.replace(key, replacement)

    # yield the generated variant
    yield variant

def main():

  # parse command line arguments
  parser = argparse.ArgumentParser(
    description='Generates a Seating Plan, e.g. for a class room, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding())
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  parser.add_argument('-t', '--title', default='Seating Plan',
                   help='the document title')
  args = parser.parse_args()

  # read the tex doc
  with open(os.path.realpath(__file__), 'r') as file:

    # skip lines until we read a latex comment marker
    for line in file:
      if len(line) > 0 and line[0] == '%': break

    # add lines to the tex_doc until we read a python docstring marker
    tex_doc = ""
    for line in file:
      if len(line) >= 3 and line[0:3] == '"""': break
      tex_doc += line

  # read the CSV doc
  with open(args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    people = [p for p in reader]

    # convert strings to integers
    for p in people:
      p['row'] = int(p['row'])
      p['column'] = int(p['column'])

    # determine height and width of the matrix
    height = max([p['row'] for p in people]) + 1
    width = max([p['column'] for p in people]) + 1

    # create the matrix cell by cell
    matrix = ""
    for y in range(height):
      for x in range(width):

        # if not the first column, add the column separator
        if x > 0:
          matrix += "&"

        # find the eventual person sitting on this place
        l = [p for p in people if p['column'] == x and p['row'] == y]
        print(l)

        # check for consistency
        if len(l) > 1:
          raise Error("Two people can not sit on the same place")

        # add person
        if len(l) == 1:
          matrix += l[0]['name']

      # end one line
      matrix += "\\\\\n"

    # replace the matrix in the tex doc
    tex_doc = tex_doc.replace('(MATRIX)', matrix)

    # write the tex dor
    with open('temp.tex', 'w') as file:
      file.write(tex_doc)

    # generate pdf from tex file
    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'temp.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    # check, if any latex errors
    retcode = proc.returncode
    if retcode != 0:

      # print error and halt
      raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

    # delete temp file
    os.remove('temp.tex')

    # rename the pdf file and then open it
    os.rename('temp.pdf', args.output)
    os.system('open ' + args.output)

# execute only if run as a script
if __name__ == "__main__":
    main()

######################################################################
# Below this comes the tex document as a multiline string            #
# Please note that we need to define it as raw string through the \\ #
######################################################################

r"""% Sitzplan. 
% Based on http://texwelt.de/wissen/fragen/13193/kommentierter-sitzplan-mit-tikz
\documentclass{scrartcl}
\usepackage[a4paper, landscape, total={25cm, 18cm}]{geometry}
\thispagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{ifthen}
\usepackage{tikz}
\usetikzlibrary{matrix}

\tikzset{
  platz/.style={
    draw,
    text width=3cm,% <- gross genug waehlen
    align=center,
    minimum height=4\baselineskip% <- gross genug waehlen
}}

\begin{document}
\begin{center}
{\Large \textbf{Sitzplan}}
\par\medskip
\noindent\begin{tikzpicture}
  \matrix(sitzplan)[
      matrix of nodes,
      row sep=3mm,
      column sep=-\pgflinewidth,
%      nodes in empty cells,
      nodes={platz,anchor=center}
    ]{(MATRIX)};
\end{tikzpicture}

\end{center}
\end{document}
"""