# v2 - using tabs
from flask import *
from flask import render_template
from data_analysis import read_score_file, plot_hist, calc_score_diff, plot_hist_diff, partition_score,\
    skew_test, normality_test, recommend_test
from effectSize import calc_eff_size
from help import helper
from werkzeug.utils import secure_filename
import os
import numpy as np
import testCase

FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['FOLDER'] = FOLDER

# defaults
DEFAULT_SEED = None
DEFAULT_EVAL_SIZE = 1

# strings to use in UI
summary_str = "Summary of statistics"
teststat_heading = "Test statistic recommendation"

def calc_score_diff(score1,score2):
	"""
	This function calculates the pairwise score difference for score1 and score2

	@param score1, score2: input scores, dictionary
	@return: score_diff, score difference, a dictionary
	"""
	score_diff = {}
	for i in score1.keys():
		score_diff[i] = score1[i]-score2[i]
	return(score_diff)


def create_test_reasons(recommended_tests):
    '''
    This function creates a dictionary of test names with reasons, given the list of test names.
    @param recommended_tests: List of tuples [('t', "t because..."), ('bootstrap', 'bootstrap because...')]
    @return: Dictionary of test names with reasons as the values
    '''
    test_reasons = {}
    for test in recommended_tests: # test is a tuple (name, reason)
        test_reasons[test[0]] = test[1]
    return test_reasons


def format_digits(num, sig_digits=5):
    str = '{:.5f}'.format(num)
    return str


def create_summary_stats_dict(tc):
    print('Score 1: mean={}, med={}, sd={}, min={}, max={}'.format(tc.eda.summaryStat_score1.mu,
                                                                             tc.eda.summaryStat_score1.med,
                                                                             tc.eda.summaryStat_score1.sd,
                                                                             tc.eda.summaryStat_score1.min_val,
                                                                             tc.eda.summaryStat_score1.max_val))
    summary_dict = {}
    summary_dict['score1'] = {'mean': format_digits(tc.eda.summaryStat_score1.mu),
                              'median': format_digits(tc.eda.summaryStat_score1.med),
                              'std.dev.': format_digits(tc.eda.summaryStat_score1.sd),
                              'min': format_digits(tc.eda.summaryStat_score1.min_val),
                              'max': format_digits(tc.eda.summaryStat_score1.max_val)}
    summary_dict['score2'] = {'mean': format_digits(tc.eda.summaryStat_score2.mu),
                              'median': format_digits(tc.eda.summaryStat_score2.med),
                              'std.dev.': format_digits(tc.eda.summaryStat_score2.sd),
                              'min': format_digits(tc.eda.summaryStat_score2.min_val),
                              'max': format_digits(tc.eda.summaryStat_score2.max_val)}
    summary_dict['difference'] = {'mean': format_digits(tc.eda.summaryStat_score_diff.mu),
                                 'median': format_digits(tc.eda.summaryStat_score_diff.med),
                                 'std.dev.': format_digits(tc.eda.summaryStat_score_diff.sd),
                                 'min': format_digits(tc.eda.summaryStat_score_diff.min_val),
                                 'max': format_digits(tc.eda.summaryStat_score_diff.max_val)}
    summary_dict['difference (partitioned)'] = {'mean': format_digits(tc.eda.summaryStat_score_diff_par.mu),
                                 'median': format_digits(tc.eda.summaryStat_score_diff_par.med),
                                 'std.dev.': format_digits(tc.eda.summaryStat_score_diff_par.sd),
                                 'min': format_digits(tc.eda.summaryStat_score_diff_par.min_val),
                                 'max': format_digits(tc.eda.summaryStat_score_diff_par.max_val)}
    return summary_dict


@app.route('/', methods= ["GET", "POST"])
def homepage(debug=True):
    if request.method == 'POST':
        f = request.files['system_file']  # new
        f.save(secure_filename(f.filename))  # todo: change this to 'uploads' directory

        scores1, scores2 = read_score_file(f.filename) #read_score_file("score")
        plot_hist(scores1, scores2)
        score_dif = calc_score_diff(scores1, scores2)
        eval_unit_size = request.form.get('eval_unit_size')

        # Handle case of no eval unit size
        if not eval_unit_size:
            eval_unit_size = DEFAULT_EVAL_SIZE

        sample_size = np.floor(len(list(score_dif))/float(eval_unit_size))

        # plot difference hist
        plot_hist_diff(score_dif, FOLDER)


        # target_stat is 'mean' or 'median'
        target_stat = request.form.get('target_statistic')
        effect_size_target_stat= request.form.get('effect_size_target_statistic')
        print('target stat={}\ntarget stat for effect size={}'.format(target_stat, effect_size_target_stat))

        seed = request.form.get('seed')
        if not seed:
            seed = DEFAULT_SEED

        # partition score difference and save svg
        score_diff_par = partition_score(score_dif, float(eval_unit_size),
                                         True, #shuffle
                                         seed,
                                         target_stat, # mean or median
                                         FOLDER)

        # --------------Summary Stats -------------
        ### initialize a new testCase object to use for summary statistics
        tc = testCase.testCase(scores1,
                               scores2,
                               score_dif,
                               score_diff_par,
                               sample_size,
                               FOLDER)
        tc.get_summary_stats()
        # todo make this a function for score1, score2, score_dif, score_dif_par:
        summary_stats_dict = create_summary_stats_dict(tc)
        # if debug: print('Score 1: mean={}, med={}, sd={}, min={}, max={}'.format(tc.eda.summaryStat_score1.mu,
        #                                                                tc.eda.summaryStat_score1.med,
        #                                                                tc.eda.summaryStat_score1.sd,
        #                                                                tc.eda.summaryStat_score1.min_val,
        #                                                                tc.eda.summaryStat_score1.max_val))

        # --------------Recommended Test Statistic (mean or median, by skewness test) ------------------
        mean_or_median = skew_test(score_diff_par)
        # ---------------normality test
        is_normal = normality_test(score_diff_par, alpha=0.05)
        # --------------Recommended Significance Tests -------------------------
        recommended_tests = recommend_test(mean_or_median, is_normal)

        # recommended tests reasons (temp function)
        recommended_tests_reasons = create_test_reasons(recommended_tests)

        if debug: print(recommended_tests_reasons)
        # test reason
        # if mean_or_median == 'mean' and is_normal:
        #     test_reason = "This test is appropriate for data in a normal distribution that is not skewed"
        # elif mean_or_median == 'mean':
        #     test_reason = "This test is appropriate for data that is not skewed, which uses the mean as the test statistic."


        if eval_unit_size:
            result_str = 'The following table shows the recommended tests.'
            full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
            full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
            full_filename_dif = os.path.join(app.config['FOLDER'], 'hist_score_diff.svg')
            full_filename_dif_par = os.path.join(app.config['FOLDER'], 'hist_score_diff_partitioned.svg')
            filename_str =  "input_filename: {} img1: {}, img2: {}, dif={}, dif_par={}".format(
                f.filename,
                full_filename1,
                full_filename2,
                full_filename_dif,
                full_filename_dif_par)
            print(filename_str)

            USE_JSON = False
            if USE_JSON:
                return jsonify(result=result_str,
                               hist_score1=full_filename1,
                               hist_score2=full_filename2)
            else:
                rand = np.random.randint(10000)
                if debug: print('random number to append to image url={}'.format(rand))
                rendered = render_template('tab_interface.html',
                                       file_uploaded = "File uploaded: {}".format(f.filename),
                                       eval_unit_size = eval_unit_size,
                                       result_str = result_str,
                                       summary_str = summary_str,
                                       summary_stats_dict = summary_stats_dict,
                                       teststat_heading = teststat_heading,
                                       mean_or_median = mean_or_median, # 'mean' if not skewed, 'median' if skewed.
                                       is_normal = is_normal,           # True if normal, False if not.
                                       recommended_tests = recommended_tests,  # this is a list.
                                       recommended_tests_reasons = recommended_tests_reasons, # dict with reasons
                                       #test_reason = test_reason,
                                       hist_score1=full_filename1,
                                       hist_score2=full_filename2,
                                       hist_diff= full_filename_dif,
                                       hist_diff_par= full_filename_dif_par,
                                           rand=rand)
                return rendered
        else:
            # we shouldn't get here since we used default values for the seed and eval unit size
            rendered = render_template('tab_interface.html',
                                       result_str='evaluation unit size or seed not defined',)
            return rendered
    elif request.method == 'GET':
        # You got to the main page by navigating to the URL, not by clicking submit
        return render_template('tab_interface.html',
                               help1 = helper("function 1"),
                               help2 = helper("function 2"),
                               file_uploaded = "Upload a file.",
                               recommended_tests = [],
                               recommended_tests_reasons ={},
                               summary_stats_dict = {})


@app.route('/effectsize', methods= ["GET", "POST"])
def effectsize():
    if request.method == 'POST':
        f = request.files['system_file']  # new
        f.save(secure_filename(f.filename))  # todo: change this to 'uploads' directory

        scores1, scores2 = read_score_file("score")  # todo: get actual filename
        # get dif
        score_dif = calc_score_diff(scores1, scores2)

        eval_unit_size = request.form.get('eval_unit_size')
        seed = request.form.get('seed')

        # target_stat is 'mean' or 'median'
        effect_size_target_stat= request.form.get('effect_size_target_statistic')
        print('target stat for effect size={}'.format(effect_size_target_stat))


        # TODO: make this not hardcoded
        (estimates, estimators) = calc_eff_size('not_wilcoxon', effect_size_target_stat, score_dif)
        print('Estimates: {}\nEstimators: {}'.format(estimates, estimators))
        if seed and eval_unit_size:
            result_str = 'Your results are displayed below. '\
                   + '; Seed is: ' + seed \
                   + "; Evaluation unit is: " + eval_unit_size

            full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
            full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
            filename_str =  "input_filename: {} img1: {}, img2: {}".format(f.filename, full_filename1, full_filename2)
            print(filename_str)

            USE_JSON = False
            if USE_JSON:
                return jsonify(result=result_str,
                               hist_score1=full_filename1,
                               hist_score2=full_filename2)
            else:
                rendered = render_template('tab_interface.html',
                                       result_str=result_str,
                                       hist_score1=full_filename1,
                                       hist_score2=full_filename2)
                return rendered
        else:
            return jsonify(result='Input needed for more details.')
    elif request.method == 'GET':
        # You got to the main page by navigating to the URL, not by clicking submit
            #full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
            #full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
        return render_template('tab_interface.html')

if __name__ == "__main__":
    app.debug=True
    app.run()
