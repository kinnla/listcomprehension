#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script produces a seating plan with the help of LaTeX.
The data for the plan must be given as CSV file
For help, run the script from command line with -h

example:
>> python3 sitzplan.py example.csv -e mac-roman --hspacing [3,3] -t Sitzplan -o Sitzplan

Prerequisits:
- XeTeX
- python 3.x
- PyPDF2 python module
- tested on macOS
"""

import argparse
import os
import subprocess
import PyPDF2
import csv
import locale
import ast

# symlink to library contained in repository
from lib import util

def parse_args():
  """parse command line arguments and return them as Namespace"""

  parser = argparse.ArgumentParser(
    description='Generates a Seating Plan, e.g. for a class room, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding(),
    help='the character encoding of the CSV file, e.g. mac-roman.')
  parser.add_argument('-o', '--output',
                   help='the output file name. "pdf" as file extension will be automatically added.')
  parser.add_argument('-t', '--title', default='Seating Plan',
                   help='the document title')
  parser.add_argument('--hspacing', default='',
                   help='Horizontal spacing in milimeters, e.g. as [3,0,0,3] for a plan with 5 columns')
  return parser.parse_args()


def main():

  # parse command line arguments 
  args = parse_args()

  # read the tex doc
  tex_doc = util.read_template(os.path.realpath(__file__))

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

  # check output file name
  if not args.output:
    args.output = args.csvfile

  # render and open pdf file
  util.create_pdf(tex_doc, args.output)
  os.system('open ' + args.output + ".pdf")

  
# execute only if run as a script
if __name__ == "__main__":
    main()

###########################################################
# Below this comes the tex document as a multiline string #
# We need to define it as raw string through the \\       #
###########################################################

r"""
% Sitzplan. 
% Based on http://texwelt.de/wissen/fragen/13193/kommentierter-sitzplan-mit-tikz

\documentclass{scrartcl}
\usepackage[a4paper, landscape, total={25cm, 18cm}]{geometry}
\usepackage{fontspec}
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
    minimum height=3.8\baselineskip
}}

\thispagestyle{empty}

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