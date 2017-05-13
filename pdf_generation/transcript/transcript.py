#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script produces a seating plan with the help of LaTeX.
The data for the plan must be given as CSV file
For help, run the script from command line with -h

example:
>> python3 sitzplan.py example.csv -e mac-roman --hspacing [3,3] -t "Sitzplan"

Prerequisits:
- latex
- python 3.x
- PyPDF2 python module
- tested on macOS
"""

import argparse
import os
#import subprocess
#import PyPDF2
import csv
import locale
#import ast
import re
#import time
#import shutil

from lib import util

# regex pattern, matches non number characters
NON_NUMBER = re.compile(r'[\D]+')

# regex pattern, indicates the end of a block
START_OF_BLOCK = re.compile(r'^(?!(Zusatzp|P)unkte|Team).*')

# regex pattern, indicates the end of a block
END_OF_BLOCK = re.compile(r'(Zusatzp|P)unkte*')

# regex pattern, matches both regular and additional scores
SCORE = re.compile(r'(Zusatzp|P)unkte*')

# regex pattern, matches any column regarded as part of the name
STUDENT_NAME = re.compile(r'Vorname|Nachname|Klasse')


def parse_args():
  """parse command line arguments and return them as Namespace"""

  parser = argparse.ArgumentParser(
    description='Generates a transcript, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding(),
    help='the character encoding of the CSV file, e.g. mac-roman or utf8.')
  parser.add_argument('-s', '--studentname', 
    help='the name of the student. If empty, transcripts for all students will be generated.')
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  return parser.parse_args()


def variants(template, args=None):
  """
  generates variants of a tex file from a given template.
  Eventual parameters can passed as command line arguments.
  """

  # read the CSV doc
  with open("../"+args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    # read the first line containing the column headers
    col_names = next(reader)

    # read other lines and store them in a list. Skip empty lines.
    lines = [line for line in reader if len(line) and line[0]]

  # compute maximum score
  max_score = 0
  for s in col_names:
    if s[:6] == "Punkte":
      max_score += int(NON_NUMBER.sub('', s))

  # iterate on the lines
  for line in lines:

    # init content to be inserted in the tex doc
    content = ''

    # count the student's score
    total_score = 0

    # name of the student
    student_name = ''

    # iterate on cells in line and synchronously on column names
    col_names_iterator = iter(col_names)
    for cell in line:
      col_name = next(col_names_iterator)

      # preprocessing: escape special characters for latex
      cell = cell.replace('&', '\\&')

      # if cell is part of the student's name, then concatenate and continue
      if re.match(STUDENT_NAME, col_name):
        student_name = student_name + cell + ' '
        continue

      # if start of a block, then add the project name
      if re.match(START_OF_BLOCK, col_name):
        content += col_name

      # if at the end or the start, add colum marker 
      if re.match(START_OF_BLOCK, col_name) or re.match(END_OF_BLOCK, col_name):
        content += '&'

      # in any case, add cell content
      content = content + cell + ' '
      
      # if end of block: add empty line, 
      if re.match(END_OF_BLOCK, col_name):
        content += "\\\\\n"
        content += "\hline\n"

      # if the cell contains a score, add it to the total score
      if re.match(SCORE, col_name) and NON_NUMBER.sub('', cell):
        total_score += int(NON_NUMBER.sub('', cell))

    # insert individual values into the tex document and then yield it
    tex_doc = template
    tex_doc = tex_doc.replace('(STUDENT_NAME)', student_name)
    tex_doc = tex_doc.replace('(CONTENT)', content)
    tex_doc = tex_doc.replace('(TOTAL_SCORE)', str(total_score))
    tex_doc = tex_doc.replace('(MAX_SCORE)', str(max_score))
    yield tex_doc


def main():

  # parse command line arguments 
  args = parse_args()

  # read the tex doc
  template = util.read_template(os.path.realpath(__file__))

  # create pdf
  util.create_pdf(template, args, variants(template, args))

  # open the combined pdf containing all variants
  os.system('open ' + args.output)

# execute only if run as a script
if __name__ == "__main__":
    main()

######################################################################
# Below this comes the tex document as a multiline string            #
# Please note that we need to define it as raw string through the \\ #
######################################################################

r"""
% Transcript. 

\documentclass [a4paper, 11pt] {article}
\usepackage[a4paper, total={15cm, 25cm}]{geometry}
\pagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{ifthen}

\begin{document}

\begin{centering}
Gymnasium Tiergarten, Schuljahr 2016/17\\
\par\medskip
\textbf{\Large Informatik Wahlpflicht, Klassenstufe 9}
\par\medskip
Übersicht über die mündliche Noten von \textbf{(STUDENT_NAME)}, Stand 11.5.2017\\
\par \medskip
\end{centering}
\hrule
\par\medskip
\begin{centering}
\begin{tabular}{|p{4cm}|p{8cm}|p{2cm}|}
\hline
\textbf{Abgabe} & \textbf{Bewertung} & \textbf{Punkte}\\
\hline
(CONTENT)
\end{tabular}
\end{centering}
\hrule
\par\medskip
\textbf{Gesamtpunktzahl}: (TOTAL_SCORE) von (MAX_SCORE)
\par\medskip
\hrule

\footnotesize{* Zusatzaufgabe}
\end{document}
"""