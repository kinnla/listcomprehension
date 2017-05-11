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
import subprocess
import PyPDF2
import csv
import locale
import ast
import re
import time
import shutil

# regex pattern, matches non number characters
NON_NUMBER = re.compile(r'[^\d]+')

# regex pattern, indicates the end of a block
END_OF_BLOCK = re.compile(r'Klasse|(Zusatzp|P)unkte*')

# regex pattern, matches both regular and additional scores
SCORE = re.compile(r'(Zusatzp|P)unkte*')

def main():

  # parse command line arguments
  parser = argparse.ArgumentParser(
    description='Generates a transcript, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding(),
    help='the character encoding of the CSV file, e.g. mac-roman or utf8.')
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  args = parser.parse_args()

  # read the tex doc
  with open(os.path.realpath(__file__), 'r') as file:

    # skip lines until we read a latex comment marker
    for line in file:
      if len(line) > 0 and line[0] == '%': break

    # add lines to the template until we read a python docstring marker
    template = ""
    for line in file:
      if len(line) >= 3 and line[0:3] == '"""': break
      template += line

  # read the CSV doc
  with open(args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    # read the first line containing the column headers
    col_names = next(reader)

    # compute maximum score
    max_score = 0
    for s in col_names:
      if s[:6] == "Punkte":
        max_score += int(NON_NUMBER.sub('', s))

    # we need a counter to name the temp PDF files
    counter = 0

    # Merger to collect the temp PDF files
    merger = PyPDF2.PdfFileMerger()

    # create temp directory
    temp_dir = "temp" + str(time.time())
    os.makedirs(temp_dir)
    os.chdir(temp_dir)

    # read CSV line by line
    for line in reader:

      # check for empty line
      if len(line) == 0 or line[0] == '':
        continue

      # init content to be inserted in the tex doc
      content = "\\noindent\\\\\n"

      # count the student's score
      total_score = 0

      # iterate on cells in line and synchronously on column names
      col_names_iterator = iter(col_names)
      for cell in line:
        col_name = next(col_names_iterator)

        # add cell to content
        content += "\\textbf{{{name}}}: ".format(name=col_name)
        content += cell
        content += "\\\\\n"
        
        # if end of block: add empty line, 
        if re.match(END_OF_BLOCK, col_name):
          content += "\\\\\n"

        # if the cell contains a score, add it to the total score
        if re.match(SCORE, col_name):
          if NON_NUMBER.sub('', cell):
            total_score += int(NON_NUMBER.sub('', cell))

      # line parsing complete
      # postprocessing: escape special characters in latex
      content = content.replace('&', '\\&')

      # copy template
      tex_doc = str(template)

      # insert individual values into the tex document
      tex_doc = tex_doc.replace('(CONTENT)', content)
      tex_doc = tex_doc.replace('(TOTAL_SCORE)', str(total_score))
      tex_doc = tex_doc.replace('(MAX_SCORE)', str(max_score))

      # increment counter and define file names
      counter += 1
      tex_file = str(counter) + ".tex"
      pdf_file = str(counter) + ".pdf"

      # write current variant as temp file
      with open(tex_file, 'w') as file:
        file.write(tex_doc)

      # generate pdf from tex file
      cmd = ['pdflatex', '-interaction', 'batchmode', tex_file]
      proc = subprocess.Popen(cmd)
      proc.communicate()

      # check, if any latex errors
      retcode = proc.returncode
      if retcode != 0:

        # print error and halt
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

      # append temp file to merger
      merger.append(pdf_file)

  # CSV parsing complete
  # delete output file in case it exists
  if os.path.isfile(args.output):
    os.remove(args.output)

  # merge the pdf files, write the result and clean up
  os.chdir("..")
  with open(args.output, 'wb') as file:
    merger.write(file)
    shutil.rmtree(temp_dir)

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
Übersicht über die mündliche Noten, Stand 11.5.2017\\
\par \medskip
\end{centering}
\hrule
\par\medskip

(CONTENT)
\hrule
\par\medskip
\textbf{Gesamtpunktzahl}: (TOTAL_SCORE) von (MAX_SCORE)
\par\medskip
\hrule

\footnotesize{* Zusatzaufgabe}
\end{document}
"""