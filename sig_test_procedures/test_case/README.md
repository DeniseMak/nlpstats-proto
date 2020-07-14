# Test case for data_analysis.py
## Input file
The input file should be two columns of scores, separated by whitespace, like the following:

> 0.1352 0.1552

> 0.5326 0.2356

> 0.2672 0.2534

> ....

I included a test score file called *score*, which has 2001 rows of BLEU scores for 2 MT systems from WMT 2018. 

## Reading input file
The function `read_score_file(score_file)` will read the input score file line by line, split each line by whitespace and save the two scores into two dictionaries. The two scores are named *score1* and *score2*.

## Plotting histograms
We will have three histograms for *score1* and *score2* and *score_diff* (their pairwise differences). The function `calc_score_diff(score1,score2)` calculates their pairwise differences and return a dictionary *score_diff*.

The function `plot_hist(score1,score2)` plots two separate histograms for *score1* and *score2*. The sample mean and median are also shown in the plots as vertical dashed (--) and dash-dotted (-.) lines. 

The function `plot_hist_diff(score_diff)` plots the histogram of *score_diff*.

These two plot functions save the plots in the format of `.svg` in the current directory.

## Partitioning score difference
The function `partition_score(score_diff, eval_unit_size, shuffled, method)` splits *score_diff* into evaluation units, of which the size is specified by the user. The user can also specify whether they want to reshuffle *score_diff* first and what method they want to use for calculation (mean or median). This function will also plot the histogram of the partitioned *score_diff*.

## Normality test
The function `normality_test(score,alpha)` will conduct Shapiro-Wilks normality test for *score_diff* at a specified significance level `alpha`. The return value is a boolean, where `True` indicates normality and `False' indicates non-normality.

## Skewness check
The function `skew_test(score)` checks whether the distribution of *score_diff* is skewed in order to determine a good measure for central tendency. Note that here mean or median has nothing to do with the method of calculation in evaluation unit partitioning. The rules of thumb are:
1. abs(skewness) > 1: highly skewed, use `median`.
2. 0.5 <= abs(skewness) < 1: moderately skewed, use `median`.
3. abs(skewness) < 0.5: roughly symmetric, use `mean` or `median`.

## Recommending significance tests
The function `recommend_test` recommends a list of significance tests based on the results given before (from functions `skew_test` and `normality_test`):
1. If normal, use `t test` (other tests are also applicable but have lower power)
2. If not normal but `mean` is a good measdure for central tendency, use:
    1. bootstrap test bassed on mean (t ratios) or medians
    2. sign test
    3. sign test calibrated by permutation (based on mean or median)
    4. Wilcoxon signed rank test 
    5. t test (may be okay for large samples)
3. If not normal and highly skewed, use:
    1. bootstrap test based on median
    2. sign test
    3. sign test calibrated by permutation (based on median)
    4. Wilcoxon signed rank test

## Running the script
The script can be tested in command line: 

`python data_analysis.py <sys.argv[1]> <sys.argv[2]> <sys.argv[3]> <sys.argv[4]> <sys.argv[5]>`

where 
* `<sys.argv[1]>` = `score_file`
* `<sys.argv[2]>` = `eval_unit_size` (for `partition_score`)
* `<sys.argv[3]>` = `shuffled` (for `partition_score`)
* `<sys.argv[4]>` = `method` (for `partition_score`)
* `<sys.argv[5]>` = `alpha` (for `normality_test`)

For example, run the following:

`python data_analysis.py score 1 False mean 0.05`

The output should be:

> Is the difference of the two scores normal: False.

> Recommended measure for central tendency: mean.

> List of recommended tests:  bootstrap sign permutation wilcoxon t.

The saved plots are in `sig_test_procedures/test_case`.


