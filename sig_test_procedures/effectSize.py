# imports

import numpy as np
import random
from scipy import stats
import itertools




def calc_eff_size(recommended_test, test_param, score1, score2):
	if test_param == 'mean': # use cohen d or hedges g
		d = cohend(score1, score2)
		eff_size_estimate = [round(d,4),round(hedgesg(d,score1,score2),4),round(glassdelta(score1,score2),4)]
		eff_size_estimator = ['Cohen\'s d','Hedges\'s g', 'Glass\' delta']

	if recommended_test == 'wilcoxon':
		eff_size_estimate = [wilcoxon_r(score1,score2)]
		eff_size_estimator = ['r']

	if recommended_test != 'wilcoxon' and test_param == 'median':
		eff_size_estimate = [hodgeslehmann(score1,score2)]
		eff_size_estimator = ['HL (unstandardized)']

	return((eff_size_estimate,eff_size_estimator))



def cohend(score1, score2):
	x = np.array(list(score1.values()))
	y = np.array(list(score2.values()))
	z = x-y

	return(z.mean()/np.sqrt(np.var(z,ddof=1)))

def hedgesg(d,score1,score2):
	n1 = len(np.array(list(score1.values())))
	n2 = len(np.array(list(score2.values())))

	if n1 != n2:
		return None
	else:
		J = 1-(3/(4*n1-9))
		return(d*J)


def glassdelta(score1,score2):
	"""
	This function calculates the Glass' delta for the two scores, where we assume score1 is the baseline
	"""
	x = np.array(list(score1.values()))
	y = np.array(list(score2.values()))
	z = x-y

	return(z.mean()/np.sqrt(np.var(x,ddof=1)))


def wilcoxon_r(score1,score2):
	z = np.array(list(score1.values()))-np.array(list(score2.values()))
	ties = []
	z_rank = stats.rankdata(z,method='average')
	for i in range(0,len(z_rank)):
		if i-np.floor(i)==0.5:
			ties.append(i)
		if z[i]<0:
			z_rank[i] = -z_rank[i]

	w_p = 0
	w_m = 0
	for i in z_rank:
		if i>0:
			w_p+=i
		if i<0:
			w_m+=-i

	mu_w = len(z)*(len(z)+1)/4
	sigma_w = np.sqrt(len(z)*(len(z)+1)*(2*len(z)+1)/24)
	z_score = (np.max([w_p,w_m])-mu_w)/sigma_w

	return(z_score/np.sqrt(len(z)))



def hodgeslehmann(score1,score2):
	z = np.array(list(score1.values()))-np.array(list(score2.values()))
	z_pair = list(itertools.combinations(z, 2))

	z_pair_average = []
	for i in z_pair:
		z_pair_average.append(np.mean(i))

	return(np.median(z_pair_average))


