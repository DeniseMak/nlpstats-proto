# imports
import numpy as np
from scipy import stats
from statsmodels.stats.descriptivestats import sign_test




def run_sig_test(recommended_test, score, alpha=0.05, mu=0,B=2000):
	if isinstance(score,dict):
		x = np.array(list(score.values()))
	else:
		x = score
		
	test_stats_value = 0
	pval = 0

	# already implemented sig tests
	if recommended_test == 't':
		test_stats_value, pval = stats.ttest_1samp(x,mu)
	if recommended_test == 'wilcoxon':
		test_stats_value, pval = stats.wilcoxon(x)
	if recommended_test == 'sign':
		test_stats_value, pval = sign_test(x)

	# self implemented sig tests
	if recommended_test == 'bootstrap':
		test_stats_value, pval = bootstrap_test(x,alpha,mu,B)

	if recommended_test == 'bootstrap_med':
		test_stats_value, pval = bootstrap_test(x,alpha,mu,B,method='median')

	if recommended_test == 'permutation':
		test_stats_value, pval = permutation_test(x,alpha,mu,B)

	if recommended_test == 'permutation_med':
		test_stats_value, pval = permutation_test(x,alpha,mu,B,method='median')


	return((test_stats_value, pval, pval < 0.05))

def bootstrap_test(score, alpha, mu, B, method='mean'):
	return((0.0,0.0))


def permutation_test(score, alpha, mu, B, method='mean'):
	return((0.0,0.0))