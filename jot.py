# define functions

def clean(string):
	return string.replace("$","\$").replace("&","\&")


# import libraries

import sys															# for reading command line arguments

# print welcome message

print "Jot Version 1.0. Copyright 2011 Shubhro Saha"

# prepare input file

try:
	f = open(sys.argv[1], 'r').readlines()
except:
	print "Jot input file not found. Please be sure to pass in the jot file name as a command-line argument."
	sys.exit()

# iterate over each line of input file and add LaTeX commands

output = """
\documentclass[10pt,a4paper]{article}
\usepackage{fancyhdr}
\usepackage[headings]{fullpage}
\usepackage{graphicx}
\lhead{\\rightmark}
\\rhead{\\thepage}

\usepackage{calc}

\\newlength{\imgwidth}

\\newcommand\scalegraphics[1]{%   
    \settowidth{\imgwidth}{\includegraphics{#1}}%
    \setlength{\imgwidth}{\minof{\imgwidth}{\\textwidth - 200pt}}%
    \includegraphics[width=\imgwidth]{#1}%
}




"""
	
output += """
\\title{"""+f[0][:-1]+"""}
\\author{"""+f[1][:-1]+"""}
\setlength{\parindent}{0pt} 
\setlength{\parskip}{2ex} \n"""

output += """
\\begin{document}
\maketitle
\\newpage

\\tableofcontents

\\newpage \n \n"""

isList = False
lineDone = False

i = 2
while (i < len(f)):
	
	lineDone = False
	line = f[i]
	i = i + 1
	lineArray = line.split(" ")
	
	if ("_image" in line):											# Image
		
		url = f[i][:-1]
		caption = clean(f[i+1])[:-1]
	
		output +="""
		
			\\begin{figure}[!htbp]
			\\begin{center}
			\scalegraphics{"""+url+"""}
			\caption{"""+caption+"""}
			\end{center}
			\label{fig:"""+url+"""}
			\end{figure}
		
		"""
		
		i = i + 2
		continue
		
	if (lineArray[0] == "\n"):										# Empty Line
		
		if (isList == True):
			isList = False
			output += "\end{itemize} \n"
		else:
			output += " \n"
		
	if (len(lineArray) > 1 and lineArray[0] + lineArray[1] == "__"):	# Sub-Section
		output += "\subsection{"+clean(line[4:-1])+"}" + " \n"
		continue
		
	if (lineArray[0] == "_"):										# Section
		output += "\section{"+clean(line[2:-1])+"}" + "\n"
		continue
		
	if (lineArray[0] == "-"):										# List
		
		if (isList == False):
			isList = True
			output += "\\begin{itemize} \n"
		output += "\item " + clean(line[2:])
		continue
		
	output += clean(line)

if (isList == True):
	isList = False
	output += "\end{itemize} \n"

output += "\n \end{document}"
fOutput = open('jotoutput.tex', 'w')
fOutput.write(output)

print "Operation Complete."