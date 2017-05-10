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

def main():

  # parse command line arguments
  parser = argparse.ArgumentParser(
    description='Generates a transcript, based on a CSV spread sheet and generates a PDF.')
  parser.add_argument('csvfile', help='the csv file containing the input')
  parser.add_argument('-e', '--encoding', default=locale.getpreferredencoding(),
    help='the character encoding of the CSV file, e.g. mac-roman or utf8.')
  parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
  parser.add_argument('-t', '--title', default='Transcript',
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

  # replace the document title
  tex_doc = tex_doc.replace('(TITLE)', args.title)

  # read the CSV doc
  with open(args.csvfile, encoding=args.encoding, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    
    # convert strings to integers
    tex = "\\noindent\\\\\n"
    start = True
    line_nr = 0
    for line in reader:
      if start:
        col_names = line
        start=False
        continue

      punkte=0
      i=0
      for col in line:

        # check for empty line
        if col == '' and i == 0:
          break

        tex = tex + "\\textbf{" + col_names[i] + "}: "
        tex = tex + col
        tex += "\\\\\n"
        
        if col_names[i][:6] == 'Punkte' or col_names[i][:6] == "Klasse":
          tex += "\\\\\n"
        if col_names[i][:6] == 'Punkte':
          try:
            punkte += int(col)
          except:
            print ("inconsistent data in line: " + str(line_nr) + " , col: " + str(i))
        i+=1

      tex = tex + "\\textbf{Punkte Gesamt}: "
      tex += str(punkte)
      tex += "\\pagebreak\\\\\n"

      line_nr += 1

  # postprocessing
  tex = tex.replace('&', '\\&')

  # replace the matrix in the tex doc
  tex_doc = tex_doc.replace('(CONTENT)', tex)

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
% Transcript. 

\documentclass{scrartcl}
\usepackage[a4paper, total={18cm, 25cm}]{geometry}
\thispagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{bbding}
\usepackage{graphicx}
\usepackage{ifthen}

\begin{document}
{\Large \textbf{(TITLE)}}
\par\medskip
(CONTENT)
\end{document}
"""