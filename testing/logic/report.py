import os

report_string = """
% https://www.scivision.dev/include-svg-vector-latex/
% This example contains a syntax error.
% https://www.checkbot.io/article/web-page-screenshots-with-svg/
\\documentclass{article}
\\usepackage[clean]{svg}

\\begin{document}

\\begin{figure}
    \\centering
    \\includesvg[width=0.6\columnwidth]{fig.svg}
\\end{figure}

\\end{document}
"""

os.system("echo % > user/report.tex")
for line in report_string.split("\n"):
  os.system("echo " + line + " >> user/report.tex")
os.system(" ")
