# imports
import numpy as np
import os
import sys
import random
from scipy import stats
import sigTesting
from statsmodels.stats.descriptivestats import sign_test
import matplotlib.pyplot as plt


def post_power_analysis(sig_test_name, score1, score2, step_size, mu=0, B=2000, alpha=0.05):
	x = np.array(list(score1.values()))
	y = np.array(list(score2.values()))
	z = x-y

	sample_sizes = np.arange(50, len(z), step_size)
	power_sampsizes = {}

	
	for i in sample_sizes:
		count = 0
		for b in range(0,B):
			z_b = np.random.choice(z, i, replace=True)
			(test_stats, pval, rejection) = sigTesting.run_sig_test(sig_test_name, z_b, alpha, mu,B)
			if rejection:
				count+=1
		power_sampsizes[i] = float(count)/B


	x = list(power_sampsizes.keys())
	y = list(power_sampsizes.values())
	plt.figure()
	plt.plot(x,y)
	plt.xlabel("Sample Size",fontsize=18)
	plt.ylabel("Power",fontsize=18)
	plt.title("Power against Different Sample Sizes",fontsize=18)

	if not os.path.exists('figures'):
		os.makedirs('figures')

	plt.savefig('figures/power_samplesizes.svg',dpi=500)

	return(power_sampsizes)

