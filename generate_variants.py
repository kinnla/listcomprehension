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
		description='Generates variants from an embedded tex doc and compiles them to a combined PDF.')
	parser.add_argument('-v', '--variants', default='1', type=int,
                   help='the number of variants to be created')
	parser.add_argument('-o', '--output', default=__file__+'.pdf',
                   help='the output file name')
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

	# we need a counter to name the temp PDF files
	counter = 0

	# Merger to collect the temp PDF files
	merger = PyPDF2.PdfFileMerger()

	# create temp directory
	temp_dir = "temp" + str(time.time())
	os.makedirs(temp_dir)
	os.chdir(temp_dir)

	# iterate on the variants
	for v in variants(tex_doc, args.variants):

		# increment counter and define file names
		counter += 1
		tex_file = str(counter) + ".tex"
		pdf_file = str(counter) + ".pdf"

		# write current variant as temp file
		with open(tex_file, 'w') as file:
			file.write(v)

		# generate pdf from tex file
		cmd = ['pdflatex', '-interaction', 'batchmode', tex_file]
		proc = subprocess.Popen(cmd)
		proc.communicate()

		# check, if any latex errors
		retcode = proc.returncode
		if retcode != 0:

			# print error and halt
		    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

		# compile again in order to produce the grade table
		proc = subprocess.Popen(cmd)
		proc.communicate()

		# append temp file to merger
		merger.append(pdf_file)

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
% Test Mathe 9b 2.5.2017
\documentclass [a4paper,ngerman,11pt]{exam}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage {ngerman}
\usepackage{gensymb}
\usepackage [utf8]{inputenc}
\usepackage{tabularx}

\pointpoints{Punkt}{Punkte}
\bonuspointpoints{Bonuspunkt}{Bonuspunkte}
\renewcommand{\solutiontitle}{\noindent\textbf{Lösung:}%
\enspace}

\chqword{Frage}
\chpgword{Seite}
\chpword{Punkte}
\chbpword{Bonus Punkte}
\chsword{Erreicht}
\chtword{Gesamt}

\hpword{Punkte:} % Punktetabelle
\hsword{Ergebnis:}
\hqword{Aufgabe:}
\htword{Summe}

\begin{document}
\noindent {\bf Name}:\hspace{3cm}{\bf Erstkorrektor:}\hspace{3cm}{\bf Zweitkorrektor}:\\
\hrule

\begin{center}
{\large\bf Fake Test zur letzten Stunde}
\end{center}
Gymnasium Tiergarten\hfill 2. Mai 2017\\
Klasse 9b, Mathematik\hfill Bearbeitungszeit: 15 Minuten
\begin{center}
\addpoints\gradetable[h][questions] 
\end{center}
\hrule
\medskip

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{questions}

\question Wandle die Funktion $f(x) = (NORMALFORM)$ nach der Methode, die wir in der letzten Stunde gelernt haben, in Scheitelpunktform um.
\begin{parts}
\part[6] Schreibe die zugehörigen Werte in die Tabelle.
\begin{center}
\def\arraystretch{1.5}
\begin{tabular}{|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.5cm}|p{2.2cm}|}
\hline
$b$ & $c$ & $\frac{b}{2}$ & $\left(\frac{b}{2}\right)^2$ & $d=-\frac{b}{2}$ & $e=c-\left(\frac{b}{2}\right)^2$ \\
\hline
& & & & &\\
\hline
\end{tabular}
\end{center}
\part[2] Notiere die Funktionsgleichung in Scheitelpunktform.\\[5mm]
$f'(x)=$
\vspace{1cm}
\part[2] Überprüfe Dein Ergebnis, indem Du die Funktionswerte für $x=0$ und $x=1$ ausrechnest.
\begin{center}
\def\arraystretch{1.5}
\begin{tabular}{|p{1.2cm}|p{1.2cm}|p{1.2cm}|}
\hline
 & $f(x)$ & $f'(x)$\\
\hline
$x=0$ & & \\
\hline
$x=1$ & & \\
\hline
\end{tabular}
\end{center}
\end{parts}

\question Schreibe die Terme so auf, wie man sie spricht. Zum Beispiel liest man $3,5=7$ als \emph{drei Komma fünf gleich sieben}.\\
\vspace{2mm}
\begin{parts}\itemsep=1cm
\part[2] $(2A)$
\part[2] $(2B)$
\part[2] $(2C)$
\part[2] $(2D)$
\end{parts}
\vspace{3mm}

\question[0] Optional: Write the terms from the previous exercise in English language.

\end{questions}
\end{document}
"""
