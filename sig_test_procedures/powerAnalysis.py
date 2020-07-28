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


def post_power_analysis(sig_test_name, sim_method, score, step_size, dist_name = 'normal', starting_size=30, output_dir='', mu=0, B=200, alpha=0.05):
	z = np.array(list(score.values()))
	sample_sizes = np.arange(starting_size, len(z), step_size)
	power_sampsizes = {}

	if sim_method == "montecarlo": 
		if dist_name == 'normal': # currently only implement for normal dist.
			mu_hat = np.mean(z)
			var_hat = np.var(z,ddof=1)
			n = len(z)
			for i in sample_sizes:
				count = 0
				for b in range(0,B):
					z_b = np.random.normal(loc=mu_hat,scale=np.sqrt(var_hat),size=int(i))
					(test_stats, pval) = stats.ttest_1samp(z_b,mu)
					if(pval<alpha):
						count+=1
				power_sampsizes[i] = float(count)/B


	if sim_method == "bootstrap":
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

