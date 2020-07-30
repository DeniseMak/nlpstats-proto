import os

def gen_report(options: dict, string: str):
  report_string = "\n".join(["""
\\documentclass{article}


\\begin{document}
""", # Preamble

"""
Data Analysis
""", # Data Analysis

"""

""",

"""

""",

"""

""",

"""
\\end{document}
""", ])

  os.system("echo % > user/report.tex")
  for line in ascii(report_string).split("\n"):
    os.system("echo " + line + " >> user/report.tex")
  os.system("cd user && /Library/TeX/texbin/pdflatex report.tex report.pdf && && cd .. && zip -r user/r" + string +".zip user/*")
