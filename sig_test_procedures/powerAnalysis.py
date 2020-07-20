# imports
import numpy as np
import os
import sys
import random
from scipy import stats
import sigTesting
from statsmodels.stats.descriptivestats import sign_test
import matplotlib
matplotlib.use('Svg')
from matplotlib import pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'


def post_power_analysis(sig_test_name, score, step_size, output_dir='', mu=0, B=200, alpha=0.05):
	z = np.array(list(score.values()))

	sample_sizes = np.arange(50, len(z), step_size)
	power_sampsizes = {}

	
	for i in sample_sizes:
		count = 0
		for b in range(0,B):
			z_b = np.random.choice(a = z, size = int(i), replace=True)
			(test_stats, pval, rejection) = sigTesting.run_sig_test(sig_test_name, z_b, alpha, mu, B)
			if rejection:
				count+=1
		power_sampsizes[i] = float(count)/B


	x = list(power_sampsizes.keys())
	y = list(power_sampsizes.values())

	plt.figure()
	plt.plot(x,y)
	plt.xlabel("Sample Size")
	plt.ylabel("Power")
	plt.title("Power against Different Sample Sizes")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	plt.savefig(output_dir+'/power_samplesizes.svg')

	return(power_sampsizes)

