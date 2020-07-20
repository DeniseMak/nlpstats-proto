import fileReader
import dataAnalysis
import sigTesting
import testCase
import effectSize
import powerAnalysis

import sys
import time
import numpy as np


if __name__ == '__main__':

	score_file = sys.argv[1]

	### initialize a new testCase object
	testCase_new = testCase.testCase(None,None,None,None,None)

	# eda
	testCase_new.eda.m = int(sys.argv[2])
	testCase_new.eda.calc_method = str(sys.argv[3])
	testCase_new.eda.isShuffled = bool(sys.argv[4])
	testCase_new.eda.randomSeed = int(sys.argv[5])

	# sig test
	testCase_new.sigTest.alpha = float(sys.argv[6])

	# power analysis
	testCase_new.power.alpha = float(sys.argv[7])
	testCase_new.power.step_size = float(sys.argv[8])

	B_boot = int(sys.argv[9])
	B_pow = int(sys.argv[10])


	# output dir
	#testCase_new.output_dir = sys.argv[10]

	### read score file
	[testCase_new.score1,testCase_new.score2] = fileReader.read_score_file(score_file)

	## data analysis
	# plot histograms
	print("------ EDA ------")
	dataAnalysis.plot_hist(testCase_new.score1, testCase_new.score2, 'figures')

	# calculate score difference
	testCase_new.calc_score_diff()

	testCase_new.sample_size = np.floor(len(list(testCase_new.score1.values()))/float(testCase_new.eda.m))

	# plot difference hist
	dataAnalysis.plot_hist_diff(testCase_new.score_diff ,'figures')

	# partition score difference
	testCase_new.score_diff_par = dataAnalysis.partition_score(testCase_new.score_diff, testCase_new.eda.m, testCase_new.eda.isShuffled, testCase_new.eda.randomSeed, testCase_new.eda.calc_method, 'figures')


	# summary statistics for score1, score1, score_diff and partitioned score_diff

	testCase_new.get_summary_stats()

	# normality test
	testCase_new.eda.normal = dataAnalysis.normality_test(testCase_new.score_diff_par, testCase_new.sigTest.alpha)

	# skewness test
	testCase_new.eda.testParam = dataAnalysis.skew_test(testCase_new.score_diff_par)

	# recommend tests
	recommended_tests = dataAnalysis.recommend_test(testCase_new.eda.testParam,testCase_new.eda.normal)
	testCase_new.sigTest.testName = recommended_tests[0] 
	testCase_new.eda.testName = testCase_new.sigTest.testName

	print('Sample size after partitioning is: '+str(testCase_new.sample_size))
	print('recommended tests: '+str(recommended_tests))
	print('the test used: '+testCase_new.sigTest.testName)
	print('normality: '+str(testCase_new.eda.normal))
	print('testing parameter: '+testCase_new.eda.testParam)

	# run sig test
	print("------ Testing ------")
	test_stat, pval, rejection = sigTesting.run_sig_test(testCase_new.sigTest.testName, testCase_new.score_diff_par, alpha = testCase_new.sigTest.alpha, B = B_boot)
	testCase_new.sigTest.test_stat = test_stat
	testCase_new.sigTest.pval = pval
	testCase_new.sigTest.rejection = rejection

	### effect size calculation

	print("------ Effect Size ------")
	eff_size_est, eff_size_name = effectSize.calc_eff_size(testCase_new.sigTest.testName, testCase_new.eda.testParam, testCase_new.score_diff_par)

	testCase_new.es.estimate = eff_size_est
	testCase_new.es.estimator = eff_size_name

	### post power analysis

	print("------ Power Analysis ------")
	start_time = time.time()

	power_sampsize = powerAnalysis.post_power_analysis(testCase_new.sigTest.testName, 
		testCase_new.score_diff_par, step_size = testCase_new.power.step_size, 
		output_dir = 'figures', B=B_pow, alpha=testCase_new.power.alpha)

	sys.stderr.write("Finished power analysis. Runtime: --- %s seconds ---" % (time.time() - start_time) + '\n')
    
	testCase_new.power.powerCurve = power_sampsize


	print('------ Report ------')

	print('test name: '+testCase_new.sigTest.testName)
	print('test statistic/CI: '+str(testCase_new.sigTest.test_stat))
	print('p-value: '+str(testCase_new.sigTest.pval))
	print('rejection of H0: '+str(testCase_new.sigTest.rejection))


	print('-----------')

	print('effect size estimates: '+str(testCase_new.es.estimate))
	print('effect size estimator: '+str(testCase_new.es.estimator))

	print('-----------')

	print('obtained power: ' + str(list(testCase_new.power.powerCurve.values())[-1]))








