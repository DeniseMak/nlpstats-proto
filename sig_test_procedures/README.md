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
* `<sys.argv[2]>` = `m` (evaluation unit size for `partition_score`)
* `<sys.argv[3]>` = `calc_method` (for `partition_score`)
* `<sys.argv[4]>` = `isShuffled` (for `partition_score`)
* `<sys.argv[5]>` = `randomSeed` (for `partition_score`)
* `<sys.argv[6]>` = `sigTest.alpha` (for sig test functions)
* `<sys.argv[7]>` = `power.alpha` (for `post_power_analysis`)
* `<sys.argv[8]>` = `power.step_size` (for `post_power_analysis`)
* `<sys.argv[9]>` = `sigTest.B` (for sig test functions)
* `<sys.argv[10]>` = `power.B` (for `post_power_analysis`)
* `<sys.argv[11]>` = `eff_size_ind` (for `calc_eff_size`, *cohend*, *hedgesg*, *wilcoxonr*, *hl*)
* `<sys.argv[12]>` = `power_method` (for `post_power_analysis`, either *bootstrap* or *montecarlo*)

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

### Partitioning score difference:
The function `partition_score(score1, score2, score_diff, eval_unit_size, shuffled, randomSeed, method, output_dir)` splits *score1, score2, score_diff* into evaluation units, of which the size is specified by the user. The user can also specify whether they want to reshuffle first, the seed used for reshuffling and the method they want to use for calculation (mean or median). This function will also plot the histogram of the partitioned *score1*, *score2* and *score_diff*.


### Skewness check:
The function `skew_test(score)` checks whether the distribution of *score_diff* is skewed in order to determine a good measure for central tendency. Note that here mean or median has nothing to do with the method of calculation in evaluation unit partitioning. The rules of thumb are:
1. abs(skewness) > 1: highly skewed, use `median`.
2. 0.5 <= abs(skewness) < 1: moderately skewed, use `median`.
3. abs(skewness) < 0.5: roughly symmetric, use `mean` or `median`.
If skewed, then the distribution is not normal for sure.

### Normality test:
The function `normality_test(score,alpha)` will conduct Shapiro-Wilks normality test for *score_diff* at a specified significance level `alpha`. The return value is a boolean, where `True` indicates normality and `False` indicates non-normality. 


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
The scripts `effectSize.py` and `powerAnalysis.py` partially provide functionalities for Stage 4. The user needs to specify what effect size index to use and what power analysis method (*bootstrap* or *montecarlo*) to use (currently only normal distribution is implemented for the Monte Carlo method).

## `main.py` test case example:
In this script, I choose the significance test to be the second in the list. If `eval_unit_size` is different (say 5), then the list of test might have different length, which may give rise to some bugs. 

Note that the power analysis part may take relatively longer time to complete.

For example, run the following:

`python main.py score 5 mean False 1 0.05 0.05 20 500 200 cohend montecarlo`

The output should be:

------ EDA ------
Sample size after partitioning is: 400.0

recommended tests: [('t', 'The student t test is most appropriate for normal sample and has the highest statistical power.'), ('bootstrap', 'The bootstrap test based on t ratios can be applied to normal sample.'), 'The sign test calibrated by permutation based on mean difference is also appropriate for normal sample, but its statistical power is relatively low due to loss of information.', ('wilcoxon', 'The Wilcoxon signed-rank test can be used for normal sample, but since it is a nonparametric test, it has relatively low statistical power. Also the null hypothesis is that the the pairwise difference has location 0.'), ('sign', 'The (exact) sign test can be used for normal sample, but it has relatively low statistical power due to loss of information.')]

the test used: t

normality: True

testing parameter: mean

------ Testing ------

------ Effect Size ------

------ Power Analysis ------

Finished power analysis. Runtime: --- 0.8795456886291504 seconds ---

------ Report ------

test name: t

test statistic/CI: 1.6931857524657286

p-value: 0.09120064130646023

rejection of H0: False

-----------

effect size estimates: 0.0847

effect size estimator: cohend

-----------

obtained power: 0.44

Power analysis method: montecarlo


Note: the final obtained power is the power level corresponding to the largest sample size. 

If the test is a bootstrap test, the return is a confidence interval and rejection boolean value, rather than a p-value. 


The saved plots are in `./figures/`.
