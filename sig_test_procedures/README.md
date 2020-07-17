# README for sig_test_procedures
## Description:
There are `8` Python files in total:
* `fileReader.py`: read the input score file
* `testCase.py`: the obeject class for testCase
* `dataAnalysis.py`: conduct pre-testing exploratory data analysis, split the score into eval units and check for test assumptions
* `sigTesting.py`: run significance testing
* `effectSize.py`: choose an effect size estimator/index and estimate effect size
* `powerAnalysis.py`: conduct post-testing power analysis

There is also a `main.py` script to test functions of the above 8 scripts, where the arguments are:
* `<sys.argv[1]>` = `score_file`
* `<sys.argv[2]>` = `eval_unit_size` (for `partition_score`)
* `<sys.argv[3]>` = `shuffled` (for `partition_score`)
* `<sys.argv[4]>` = `method` (for `partition_score`)
* `<sys.argv[5]>` = `alpha` (for `normality_test`)
* `<sys.argv[6]>` = `step_size` (for `post_power_analysis`)


## Input file:
The input file should be two columns of scores, separated by whitespace, like the following:

> 0.1352 0.1552

> 0.5326 0.2356

> 0.2672 0.2534

> ....

I included a test score file called *score*, which has 2001 rows of BLEU scores for 2 MT systems from WMT 2018. 

### Reading input file
The script `fileReader.py` will read the input score file line by line, split each line by whitespace and save the two scores into two dictionaries. The two scores are named `score1` and `score2`.

## testCase class:
The class `testCase` is an object that corresponds to a one-time testing run. It has the following attributes:
* `score1`: *dict*
* `score2`: *dict*
* `score_diff`: dict
* `testParam`: *string*, parameter to test (mean or median)
* `sigTest`: *string*, the name of the significance test to run
* `effSize`: *(float,string)*, effect size estimate and estimator name
* `powAnaly`: *dict*, post-power against different sample sizes

There is a built-in function:
* `calc_score_diff()`: calculates score difference


## Stage 2: data analysis
The script `dataAnalysis.py` conducts the pre-testing exploratory data analysis to plot histograms and check for test assumptions.

### Plotting histograms:
We will have three histograms for *score1* and *score2* and *score_diff* (their pairwise differences). The function `calc_score_diff(score1,score2)` calculates their pairwise differences and return a dictionary *score_diff*. The function `plot_hist(score1,score2)` plots two separate histograms for *score1* and *score2*. The sample mean and median are also shown in the plots as vertical dashed (--) and dash-dotted (-.) lines. 

The function `plot_hist_diff(score_diff)` plots the histogram of *score_diff*.

These two plot functions save the plots in the format of `.svg` in the directory `figures`, which is created by the script.

### Partitioning score difference:
The function `partition_score(score_diff, eval_unit_size, shuffled, method)` splits *score_diff* into evaluation units, of which the size is specified by the user. The user can also specify whether they want to reshuffle *score_diff* first and what method they want to use for calculation (mean or median). This function will also plot the histogram of the partitioned *score_diff*.

### Normality test:
The function `normality_test(score,alpha)` will conduct Shapiro-Wilks normality test for *score_diff* at a specified significance level `alpha`. The return value is a boolean, where `True` indicates normality and `False' indicates non-normality.

### Skewness check:
The function `skew_test(score)` checks whether the distribution of *score_diff* is skewed in order to determine a good measure for central tendency. Note that here mean or median has nothing to do with the method of calculation in evaluation unit partitioning. The rules of thumb are:
1. abs(skewness) > 1: highly skewed, use `median`.
2. 0.5 <= abs(skewness) < 1: moderately skewed, use `median`.
3. abs(skewness) < 0.5: roughly symmetric, use `mean` or `median`.

### Recommending significance tests:
The function `recommend_test` recommends a list of significance tests based on the results given before (from functions `skew_test` and `normality_test`):
1. If normal, use `t test` (other tests are also applicable but have lower power) <`t`>
2. If not normal but `mean` is a good measdure for central tendency, use:
    1. bootstrap test bassed on mean (t ratios) or medians <`bootstrap`>
    2. sign test <`sign`>
    3. sign test calibrated by permutation (based on mean or median) <`permutation`>
    4. Wilcoxon signed rank test <`wilcoxon`>
    5. t test (may be okay for large samples) <`t`>
3. If not normal and highly skewed, use:
    1. bootstrap test based on median <`bootstrap_med`>
    2. sign test <`sign`>
    3. sign test calibrated by permutation (based on median) <`permutation_med`>
    4. Wilcoxon signed rank test <`wilcoxon`>

## Stage 3: significance testing
The script `sigTesting.py` contains functions to run the significance testing chosen in Stage 2.


## Stage 4: reporting (effect size estimation and power analysis)
The scripts `effectSize.py` and `powerAnalysis.py` partially provide functionalities for Stage 4.

## `main.py` test case:
In this script, I choose the significance test to be the second in the list. If `eval_unit_size` is different (say 5), then the list of test might have different length, which may give rise to some bugs. 

Note that the power analysis part may take relatively longer time to complete.

For example, run the following:

`python main.py score 1 False mean 0.05 20`

The output should be:

> ['bootstrap', 'sign', 'permutation', 'wilcoxon', 't'] (this is the list of recommended tests)

> 55.0 (this is the value of test statistic. In this case the test is the sign test.)

> 0.012608304160644415 (this is the obtained p value)

> True (this is whether the test rejects the null that the location of difference is 0)

-----------

> [0.03676324583189519, 0.036749450992933884] (these are the estimates of effect size. There are two indices.)

> ["Cohen's d", "Hedges's g"] (These are the names of the effect sise indices)

The saved plots are in `./figures/`.
