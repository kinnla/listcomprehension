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
#import time
#import shutil
import csv
import locale
import ast

def main():

  # parse command line arguments
  parser = argparse.ArgumentParser(
    description='Generates a Seating Plan, e.g. for a class room, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding(),
    help='the character encoding of the CSV file, e.g. mac-roman.')
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  parser.add_argument('-t', '--title', default='Seating Plan',
                   help='the document title')
  parser.add_argument('--hspacing', default='',
                   help='Horizontal spacing in milimeters, e.g. as [3,0,0,3] for a plan with 5 columns')
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

  # replace the document title
  tex_doc = tex_doc.replace('(TITLE)', args.title)

  # read the CSV doc
  with open(args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    
    # convert strings to integers
    people = []
    for p in reader:
      p['row'] = int(p['row'])
      p['column'] = int(p['column'])
      people.append(p)

  # determine height and width of the matrix
  height = max([p['row'] for p in people]) + 1
  width = max([p['column'] for p in people]) + 1

  # parse horizontal spacing (default 3mm)
  hspacing = [3] * (width-1)
  if args.hspacing != '':
    hspacing = ast.literal_eval(args.hspacing)

  # create the matrix cell by cell
  matrix = ""
  for y in range(height):
    for x in range(width):

      # if not the first column, add the column separator
      if x > 0:
        matrix += "&"
        
        # if on the first row, add spacing
        if y == 0:
          matrix += ("[" + str(hspacing[x-1]) + "mm]")

      # find the eventual person sitting on this place
      l = [p for p in people if p['column'] == x and p['row'] == y]

      # check for consistency
      if len(l) > 1:
        raise IndexError("Two people can not sit on the same place")

      # check if a person sits here
      if len(l) == 1:
        person = l[0]

        # add person  
        matrix += '{'
        matrix += (person['name'] + r"\\")

        # create hands, if given
        if 'hands' in person:
          hands = int(person['hands'])
          matrix += hands * r"{\scalebox{.7}{\rotatebox[x=0mm, y=4mm]{-90}{\HandLeft}}}"
          matrix += "~~"

        # add string, if given
        if 'string' in person:
          matrix += person['string']

        # end this node
        matrix += '}'

    # end one line
    matrix += "\\\\\n"

  # replace the matrix in the tex doc
  tex_doc = tex_doc.replace('(MATRIX)', matrix)

  # write the tex doc
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
  #os.remove('temp.tex')

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

r"""
% Sitzplan. 
% Based on http://texwelt.de/wissen/fragen/13193/kommentierter-sitzplan-mit-tikz

\documentclass{scrartcl}
\usepackage[a4paper, landscape, total={25cm, 18cm}]{geometry}
\thispagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{bbding}
\usepackage{graphicx}
\usepackage{ifthen}
\usepackage{tikz}
\usetikzlibrary{matrix}

\tikzset{
  platz/.style={
    draw,
    text width=3cm,
    align=center,
    minimum height=4\baselineskip
}}

\begin{document}
\begin{center}
{\Large \textbf{(TITLE)}}
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