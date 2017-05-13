#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script produces transcripts from a CSV file with the help of LaTeX.
For the specific CVS data format, see the sample file
For help, run the script from command line with -h

example:
>> python3 -m transcript.transcript WP9-Master.csv -e mac-roman

Prerequisits:
- latex
- python 3.x
- PyPDF2 python module
- tested on macOS
"""

import argparse
import os
import csv
import locale
import re

from lib import util

# regex pattern, matches non number characters
NON_NUMBER = re.compile(r'[\D]+')

# regex pattern, matches characters neither dot nor digit
NON_DOT_DIGIT = re.compile(r'[\D\.]+')

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
  parser.add_argument('-s', '--studentname', default='',
    help='the name of the student. If empty, transcripts for all students will be generated.')
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  return parser.parse_args()


def compute_mark(percentage):
  """computes the mark according to the percentage"""
  if percentage <10: return '6 (ungenügend)'
  if percentage <45: return '5 (mangelhaft)'
  if percentage <60: return '4 (ausreichend)'
  if percentage <75: return '3 (befriedigend)'
  if percentage <90: return '2 (gut)'
  return '1 (sehr gut)'


def variants(template, args=None):
  """
  generates variants of a tex file from a given template.
  Eventual parameters can passed as command line arguments.
  """

  # read the CSV doc
  with open("../" + args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    # read the first line containing the column headers, and strip them.
    col_names = next(reader)
    col_names = [s.strip() for s in col_names]

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

      # preprocessing: remove whitespace and escape special characters for latex
      cell = cell.strip().replace('&', '\\&')

      # if cell is part of the student's name, then concatenate and continue
      if re.match(STUDENT_NAME, col_name):
        student_name = student_name + cell + ' '
        continue

      # if start of block: add table line, project name and date
      if re.match(START_OF_BLOCK, col_name):
        content += "\\\\\\hline\n"
        k = col_name.rfind(" ")
        content = content + col_name[:k] + "&" + col_name[k+1:]

      # if at the end or at the start, add colum marker. Add "Team:" if necessary
      if re.match(START_OF_BLOCK, col_name) or re.match(END_OF_BLOCK, col_name):
        content += '&'
      elif cell:
        content += ' Team: '

      # Add cell content. In case of a missing score: add '-'
      content += cell
      if re.match(END_OF_BLOCK, col_name) and cell == '':
        content += '-'
      
      # if end of block: add maximum score
      if re.match(END_OF_BLOCK, col_name):
        if 'Zusatz' in col_name:
          content += "/ *"
        elif NON_NUMBER.sub('', col_name):
          content += "/ " + NON_NUMBER.sub('', col_name)

      # if the cell contains a score, add it to the total score
      if re.match(SCORE, col_name) and NON_NUMBER.sub('', cell):
        total_score += int(NON_NUMBER.sub('', cell))

    # compute percentage
    percentage = total_score * 100 // max_score
    
    # insert individual values into the tex document
    tex_doc = template
    tex_doc = tex_doc.replace('(STUDENT_NAME)', student_name)
    tex_doc = tex_doc.replace('(CONTENT)', content)
    tex_doc = tex_doc.replace('(TOTAL_SCORE)', str(total_score))
    tex_doc = tex_doc.replace('(MAX_SCORE)', str(max_score))
    tex_doc = tex_doc.replace('(PERCENTAGE)', str(percentage))
    tex_doc = tex_doc.replace('(MARK)', compute_mark(percentage))

    # if want to print scores for this student, yield
    if args.studentname in student_name:
       yield tex_doc


def main():

  # parse command line arguments 
  args = parse_args()

  # read the tex doc
  template = util.read_template(os.path.realpath(__file__))

  # create pdf series
  util.create_pdf_series(template, args, variants(template, args))

  # open the combined pdf containing all variants
  os.system('open ' + args.output)

# execute only if run as a script
if __name__ == "__main__":
    main()

###########################################################
# Below this comes the tex document as a multiline string #
# We need to define it as raw string through the \\       #
###########################################################

r"""
% Transcript. 

\documentclass [a4paper, 11pt] {article}
\usepackage[a4paper, total={15cm, 25cm}]{geometry}
\pagestyle{empty}
\usepackage[utf8]{inputenc}

\makeatletter
\newcommand{\thickhline}{%
    \noalign {\ifnum 0=`}\fi \hrule height 1pt
    \futurelet \reserved@a \@xhline
}
\makeatother

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
\begin{tabular}{|p{3.2cm}|p{1.4cm}|p{8cm}|p{1.4cm}|}
\hline
\textbf{Abgabe} & \textbf{Datum} & \textbf{Bewertung} & \textbf{Punkte}
(CONTENT)\\\thickhline
 \multicolumn{3}{r}{\textbf{Gesamtpunktzahl:}} & \multicolumn{1}{l}{(TOTAL_SCORE)/ (MAX_SCORE)}\\
\end{tabular}
\par\bigskip
Das sind \textbf{(PERCENTAGE)\%} der Punkte und ergibt die Note \textbf{(MARK)}.
\end{centering}
\vfill
\hrule
\par\medskip
\noindent\footnotesize{* Zusatzaufgabe}
\end{document}
"""