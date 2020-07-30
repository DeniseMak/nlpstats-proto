import os

report_string = "\n".join([
"""
\\\\documentclass{article}


\\\\begin{document}
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
\\\\end{document}
""",
])

os.system("echo % > user/report.tex")
for line in report_string.split("\n"):
  os.system("echo " + line + " >> user/report.tex")
os.system("pdflatex user/report.tex")
