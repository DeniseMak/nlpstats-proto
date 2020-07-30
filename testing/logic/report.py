import os

def gen_report(options: dict, string: str):
  report_string = """
\\documentclass{article}

\\begin{document}

\\section{Data Analysis}

Tests indicate the following about the data in the file \\texttt{""" + options["filename"] + """}:

  \item """ + options["normality_message"] + """
\\begin{itemize}
  \\item """ + options["normality_message"] + """
  \\item """ + options["skewness_message"] + """
  \\item """ + options["test_statistic_message"] + """
\\end{itemize}

Based on this information, the following significance tests are appropriate for your data:

""" + options["significance_tests_table"] + """

\\section{Significance testing}

Requiring a significance level $\\alpha = """ + options["significance_alpha"] + """$, """ + options["bootstrap iterations"] + """ iterations for bootstraping tests, and an expected mean difference for null hypothesis mean of """ + options["expected_mean_diff"] + """ and using the """ + options["chosen_sig_test"] + """ significance test, we can conclude that you """ + options["should_reject?"] + """ the null hypothesis. The test statistic and confidence interval are """ + options["statistic/CI"] + """ respectively.

\\section{Effect Size}

\\section{Power Analysis}

\\end{document}
"""

  os.system("echo % > user/report.tex")
  for line in report_string.split("\n"):
    print(line, file=open('user/report.tex', 'a'))
  os.system("cd user && /Library/TeX/texbin/pdflatex report.tex report.pdf && echo y | rm report.aux && echo y | rm report.log && cd .. && zip -r user/r" + string +".zip user/*")
