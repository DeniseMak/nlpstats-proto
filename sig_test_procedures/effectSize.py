# imports

import numpy as np
import random
from scipy import stats



def calc_eff_size(recommended_test, test_param, score1, score2):
	if test_param == 'mean': # use cohen d or hedges g
		d = cohend(score1, score2)
		eff_size_estimate = [d,hedgesg(d,score1,score2)]
		eff_size_estimator = ['Cohen\'s d','Hedges\'s g']

	if recommended_test == 'wilcoxon':
		eff_size_estimate = [wilcoxon_z(score1,score2)]
		eff_size_estimator = ['r']

	if recommended_test != 'wilcoxon' and test_param == 'median':
		eff_size_estimate = [0]
		eff_size_estimator = ['--']

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

def wilcoxon_z(score1,score2):
	z = np.array(list(score1.values()))-np.array(list(score2.values()))
	ties = []
	z_rank = stats.rankdata(z,method='average')
	for i in range(0,len(z_rank)):
		if i-np.floor(i)==0.5:
			ties.append(i)
		if z[i]<0:
			z_rank[i] = -z_rank[i]

	w_p, w_m = 0
	for i in z_rank:
		if i>0:
			w_p+=i
		if i<0:
			w_m+=-i

	mu_w = len(z)*(len(z)+1)/4
	sigma_w = np.sqrt(len(z)*(len(z)+1)*(2*len(z)+1)/24)
	z_score = (np.max([w_p,w_m])-mu_w)/sigma_w

	return(z_score/np.sqrt(len(z)))



