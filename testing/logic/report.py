import os

def gen_report(options: dict, string: str):
  report_string = """
\\documentclass{article}


\\begin{document}

Data Analysis

\\end{document}
"""

  os.system("echo % > user/report.tex")
  for line in ascii(report_string).split("\n"):
    os.system("echo " + line + " >> user/report.tex")
  os.system("cd user && /Library/TeX/texbin/pdflatex report.tex report.pdf && echo y | rm report.aux && echo y | rm report.log && cd .. && zip -r user/r" + string +".zip user/*")
