
"""
This is a script for pre-testing exploratory data analysis. Main functionality inclues:
1. read the score file (assumes a file with two columns of numbers, each row separated by whitespace)
2. plot histograms of score1, score2 and their difference--score_diff (assumes paired sample)
3. partition the difference
"""

# imports
import os
import sys
import numpy as np
from scipy import stats
import random
import matplotlib
matplotlib.use('Svg')
from matplotlib import pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'


def plot_hist(score1, score2, output_dir):
	"""
	This is a function to plot histograms of input scores and save the plot to current directory.

	@param score1: input score1, a dictionary
	@param score1: input score2, a dictionary
	@return: none
	"""
	x = list(score1.values())
	y = list(score2.values())

	plt.figure()
	plt.hist(x, bins=np.linspace(0,1,50))
	plt.axvline(np.array(x).mean(), color='b', linestyle='--', linewidth=1, label='mean')
	plt.axvline(np.median(np.array(x)), color='r', linestyle='-.', linewidth=1, label='median')
	plt.legend(loc='upper right')
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.title("Histogram of score1")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	plt.savefig(output_dir+'/hist_score1.svg')


	plt.figure()
	plt.hist(y, bins=np.linspace(0,1,50))
	plt.axvline(np.array(y).mean(), color='b', linestyle='--', linewidth=1,label='mean')
	plt.axvline(np.median(np.array(y)), color='r', linestyle='-.', linewidth=1,label='median')
	plt.legend(loc='upper right')
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.title("Histogram of score2")

	plt.savefig(output_dir+'/hist_score2.svg')
	

def plot_hist_diff(score_diff, output_dir):
	"""
	This is a function to plot the histogram of the score difference

	@param score_diff: input score difference
	@return: none
	"""

	x = list(score_diff.values())
	plt.figure()
	plt.hist(x, bins=np.linspace(-1,1,50))
	plt.axvline(np.array(x).mean(), color='b', linestyle='--', linewidth=1, label='mean')
	plt.axvline(np.median(np.array(x)), color='r', linestyle='-.', linewidth=1, label='median')
	plt.legend(loc='upper right')
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.title("Histogram of Score Difference")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	plt.savefig(output_dir+'/hist_score_diff.svg')


def partition_score(score_diff, eval_unit_size, shuffled, randomSeed, method, output_dir):
	"""
	This function partitions the score difference with respect to the given
	evaluation unit size. Also, the user can choose to shuffle the score difference
	before partitioning.

	@param score_diff: score difference, a dictionary
	@param eval_unit_size: evaluation unit size
	@param shuffled: a boolean value indicating whether reshuffling is done
	@param method: how to calculate score in an evaluation unit (mean or median)
	@return: score_diff_new, the partitioned score difference, a dictionary
	"""
	ind = list(score_diff.keys())
	if shuffled:
		ind_shuffled = random.Random(randomSeed).shuffle(ind)
	ind_shuffled = np.array_split(ind,np.floor(len(ind)/eval_unit_size))
	ind_new = 0
	score_diff_new = {}
	for i in ind_shuffled:
		if method == "mean":
			score_diff_new[ind_new] = np.array([score_diff[x] for x in i]).mean()
		if method == "median":
			score_diff_new[ind_new] = np.median(np.array([score_diff[x] for x in i]))
		ind_new+=1

	x = list(score_diff_new.values())
	plt.figure()
	plt.hist(x, bins=np.linspace(-1,1, 50))
	plt.axvline(np.array(x).mean(), color='b', linestyle='--', linewidth=1, label='mean')
	plt.axvline(np.median(np.array(x)), color='r', linestyle='-.', linewidth=1, label='median')
	plt.legend(loc='upper right')
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.title("Histogram of Score Difference (partitioned)")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	plt.savefig(output_dir+'/hist_score_diff_partitioned.svg')

	return(score_diff_new)


def summary_stats(score):
	x = np.array(list(score.values()))



def normality_test(score, alpha=0.05):
	"""
	This function invokves the Shapiro-Wilks normality test to test whether
	the input score is normally distributed.

	@param score: input score, a dictionary
	@param alpha: significance level
	@return: whether to reject to not reject, a boolean value 
			(True: canoot reject; False: reject)
	"""
	if isinstance(alpha,float) == False:
		sys.stderr.write("Invalid input alpha value! Procedure terminated at normality test step.\n")
		return
	else:
		if alpha>1 or alpha<0:
			sys.stderr.write("Invalid input alpha value! Procedure terminated at normality test step.\n")
			return
	x = list(score.values())
	norm_test = stats.shapiro(x)
	if norm_test[1]>alpha:
		return(True)
	else:
		return(False)

def skew_test(score):
	"""
	This function is to check whether the skewness of the input score indicates
	asymmetry of the underlying distribution. This is a rule-based decision to recommend
	whether the test should be based on the mean or median to measure central tendency: 
	|skewness| > 1 : highly skewed
	|skewness| in (0.5,1) : moderately skewed
	|skewness| < 0.5 : roughly symmetric

	@param score: input score
	@return: a string of "mean" or "median"
	"""
	x = list(score.values())
	skewness = stats.skew(x)

	if abs(skewness)>1:
		return("median")
	elif abs(skewness)<1 and abs(skewness)>0.5:
		return("median")
	elif abs(skewness)<0.5:
		return("mean")


def recommend_test(test_param,is_norm):
	"""
	This function recommends a list of significance tests based on previous results.
		if normal, then use t test (other tests are also applicable)
		if not normal but mean is a good measure of central tendancy, use:
			- bootstrap test based on mean (t ratios) or medians
			- sign test
			- sign test calibrated by permutation (based on mean or median)
			- Wilcoxon signed rank test
			- t test (may be okay given large samples)
		if not normal and highly skewd, use:
			- bootstrap test for median
			- sign test
			- sign test calibrated by permutation (based on median)
			- wilcoxon signed rank test

	@param test_param: "mean" or "median"
	@param is_norm: True or False
	@return: a list of recommended test
	"""
	if is_norm==True:
		return(['t'])
	else:
		if test_param=="mean":
			return(['bootstrap','sign','permutation','wilcoxon','t'])
		else:
			return(['bootstrap_med','sign','permutation_med','wilcoxon'])

