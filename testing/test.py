
from logic.report import gen_report
import numpy as np
def download_file():
        options = {}
        options["filename"]= "3"
        options["normality_message"]= "3"
        options["skewness_message"]= "3"
        options["test_statistic_message"]= "3"
        options["significance_tests_table"]= "3"
        options["significance_alpha"] = "3"
        options["bootstrap iterations"]= "3"
        options["expected_mean_diff"]= "3"
        options["chosen_sig_test"]= "3"
        options["should_reject?"]= "3"
        options["statistic/CI"]= "3"
        rand = np.random.randint(10000)
        gen_report(options, str(rand))
  
download_file()
