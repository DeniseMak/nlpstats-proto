import fileReader
import dataAnalysis
import sigTesting
import testCase
import effectSize
import powerAnalysis

import sys


if __name__ == '__main__':

	score_file = sys.argv[1]
	eval_unit_size = int(sys.argv[2])
	shuffled = bool(sys.argv[3])
	method = str(sys.argv[4])
	alpha = float(sys.argv[5])
	step_size = int(sys.argv[6])



	### initialize a new testCase object
	testCase_new = testCase.testCase(None,None,None,None,None,None,None)

	### read score file
	[testCase_new.score1,testCase_new.score2] = fileReader.read_score_file(score_file)

	## data analysis
	# plot histograms
	dataAnalysis.plot_hist(testCase_new.score1, testCase_new.score2)

	# calculate score difference
	testCase_new.calc_score_diff()

	# plot difference hist
	dataAnalysis.plot_hist_diff(testCase_new.score_diff)

	# partition score difference
	testCase_new.score_diff = dataAnalysis.partition_score(testCase_new.score_diff, eval_unit_size, shuffled, method)

	# normality test
	norm_test_diff = dataAnalysis.normality_test(testCase_new.score_diff, alpha)

	# skewness test
	testCase_new.testParam = dataAnalysis.skew_test(testCase_new.score_diff)

	# recommend tests
	recommended_tests = dataAnalysis.recommend_test(testCase_new.testParam,norm_test_diff)


	### significance testing
	testCase_new.sigTest = recommended_tests[1] ###### TO-FIX: the recommended test should be selected by the user#####

	# run sig test
	test_stat, pval, rejection = sigTesting.run_sig_test(testCase_new.sigTest, testCase_new.score_diff)


	### effect size calculation

	eff_size_est, eff_size_name = effectSize.calc_eff_size(testCase_new.sigTest, testCase_new.testParam, testCase_new.score1, testCase_new.score2)


	### post power analysis

	power_sampsize = powerAnalysis.post_power_analysis(testCase_new.sigTest, testCase_new.score1, testCase_new.score2, step_size,B=1000)


	print(testCase_new.sigTest)
	print(recommended_tests)
	print(test_stat)
	print(pval)
	print(rejection)

	print('-------')

	print(eff_size_est)
	print(eff_size_name)








