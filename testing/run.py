# v3
from flask import *
from flask import render_template

from werkzeug.utils import secure_filename
import os
import numpy as np

# Haotian's Business Logic
from logic.test_case import testCase
from logic.help import helper
from logic.effectSize import calc_eff_size
from logic.data_analysis import read_score_file, plot_hist, calc_score_diff, plot_hist_diff, partition_score,\
skew_test, normality_test, recommend_test
from logic.sig_testing import run_sig_test

import logic.sig_testing
import logic.power_analysis

FOLDER = os.path.join('user')
from logic.power_analysis import post_power_analysis


app = Flask(__name__)
app.config['FOLDER'] = FOLDER

# defaults
DEFAULT_SEED = None
DEFAULT_EVAL_SIZE = 1

# template filename
# Note: "tab_inteface2.html" has histograms before recommendations
template_filename = "tab_interface.html"

# strings to use in UI
summary_str = "Summary of statistics"
teststat_heading = "Test statistic recommendation"
sig_test_heading = 'You can choose from the following significance tests'
estimators = {"cohend": "This function calculates the Cohen's d effect size estimator.",
              "hedgesg": "This function takes the Cohen's d estimate as an input and calculates the Hedges's g.",
              "wilcoxon_r": "This function calculates the standardized z-score (r) for the Wilcoxon signed-rank test.",
              "hodgeslehmann": "This function estimates the Hodges-Lehmann estimator for the input score."}

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
        # ------- Test if 'last_tab' was sent
        last_tab_clicked = request.form.get('last_tab')
        # todo: make this a cookie
        last_tab_name_clicked = 'Data Analysis' #request.form.get('last_tab_name')
        print("***** LAST TAB: {}".format(last_tab_clicked))
        print("***** LAST TAB: {}".format(last_tab_name_clicked))

        eval_unit_size = request.form.get('eval_unit_size')

        # Handle case of no eval unit size
        if not eval_unit_size:
            eval_unit_size = DEFAULT_EVAL_SIZE

        # target_stat is 'mean' or 'median'
        eval_unit_stat = request.form.get('target_statistic')
        print('eval_unit_stat={}'.format(eval_unit_stat))

        seed = request.form.get('seed')
        if not seed:
            shuffle = False
            # seed = DEFAULT_SEED
        else:
            shuffle = True

        # ------- File ----------------
        f = request.files['system_file']  # new
        have_file = False
        have_filename = False
        if f.filename:
            have_filename = True
            data_filename = f.filename
            f.save(FOLDER + "/" + secure_filename(data_filename))
            have_file = True # assume the above worked
        elif request.cookies.get('fileName'):
            data_filename = request.cookies.get('fileName')
            have_filename = True
        else:
            # no filename, print error message
            print('ERROR: submitted without filename! You must resubmit!')

        if have_filename:
            if debug: print('have filename:{}'.format(data_filename))
            try:
                scores1, scores2 = read_score_file(FOLDER + "/" + data_filename)
                if len(scores1) > 0 and len(scores2):
                    score_dif = calc_score_diff(scores1, scores2)
                # todo: display how many samples there are
                    sample_size = np.floor(len(list(score_dif)) / float(eval_unit_size))
                    if debug: print('SAMPLE SIZE (#eval units)={}'.format(sample_size))
                    have_file = True
            except:
                print('Exception occurred reading file: filename={}'.format(data_filename))

        if have_file:
            # partition score difference and save svg
            score_diff_par = partition_score(scores1, scores2, score_dif, float(eval_unit_size),
                                         shuffle, # shuffle if we have seed
                                         seed,
                                         eval_unit_stat, # mean or median
                                         FOLDER)

            # --------------Summary Stats -------------
            ### initialize a new testCase object to use for summary statistics
            tc = testCase(scores1,
                                   scores2,
                                   score_dif,
                                   score_diff_par[2],#score_diff_par,
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
            mean_or_median = skew_test(score_diff_par[2])
            # ---------------normality test
            # todo: add alpha parameter
            is_normal = normality_test(score_diff_par[2], alpha=0.05)
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

            full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1_partitioned.svg')
            full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2_partitioned.svg')
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
                return jsonify(result=sig_test_heading,
                               hist_score1=full_filename1,
                               hist_score2=full_filename2)
            else:
                rand = np.random.randint(10000)
                if debug: print('random number to append to image url={}'.format(rand))


                rendered = render_template(template_filename,
                                           file_uploaded = "File uploaded: {}".format(f.filename),
                                           last_tab_name_clicked=last_tab_name_clicked,
                                           eval_unit_size = eval_unit_size,
                                           eval_unit_stat = eval_unit_stat,
                                           shuffle_seed = seed,
                                           sig_test_heading = sig_test_heading,
                                           summary_str = summary_str,
                                           summary_stats_dict = summary_stats_dict,
                                           teststat_heading = teststat_heading,
                                           sigtest_heading = sig_test_heading,
                                           mean_or_median = mean_or_median,  # 'mean' if not skewed, 'median' if skewed.
                                           is_normal = is_normal,  # True if normal, False if not.
                                           recommended_tests = recommended_tests,  # this is a list.
                                           recommended_tests_reasons = recommended_tests_reasons,  # dict with reasons
                                           hist_score1=full_filename1,
                                           hist_score2=full_filename2,
                                           hist_diff= full_filename_dif,
                                           hist_diff_par= full_filename_dif_par,
                                           rand=rand,  # rand is for image URL to force reload (avoid caching)
                                           # specific to effect size test
                                           effect_size_estimators = estimators
                                           )
                resp = make_response(rendered)

                # -------------- Set all cookies -------------
                if f.filename:
                    resp.set_cookie('fileName', f.filename)
                resp.set_cookie('eval_unit_size', eval_unit_size)
                resp.set_cookie('eval_unit_stat', eval_unit_stat)
                resp.set_cookie('shuffle_seed', seed)

                resp.set_cookie('summary_str', summary_str)
                serialized_summary_stats_dict = json.dumps(summary_stats_dict)
                resp.set_cookie('summary_stats_dict', serialized_summary_stats_dict)

                resp.set_cookie('teststat_heading', teststat_heading)
                resp.set_cookie('mean_or_median', mean_or_median)
                resp.set_cookie('is_normal', json.dumps(is_normal))

                resp.set_cookie('sig_test_heading', sig_test_heading)
                serialized_recommended_tests = json.dumps(recommended_tests)
                serialized_recommended_tests_reasons = json.dumps(recommended_tests_reasons)
                resp.set_cookie('recommended_tests', serialized_recommended_tests)
                resp.set_cookie('recommended_test_reasons', serialized_recommended_tests_reasons)

                resp.set_cookie('hist_score1', full_filename1)
                resp.set_cookie('hist_score2', full_filename2)
                resp.set_cookie('hist_diff', full_filename_dif)
                resp.set_cookie('hist_diff_par', full_filename_dif_par)
                return resp   # return rendered
        else:
            # no file
            rendered = render_template(template_filename,
                                       error_str='You must submit a file.',)
            return rendered
    elif request.method == 'GET':
        # You got to the main page by navigating to the URL, not by clicking submit
        return render_template(template_filename,
                               help1 = helper("function 1"),
                               help2 = helper("function 2"),
                               file_uploaded = "Upload a file.",
                               recommended_tests = [],
                               recommended_tests_reasons ={},
                               summary_stats_dict = {})

# ********************************************************************************************
#   SIGNIFICANCE TEST
# ********************************************************************************************
@app.route('/sig_test', methods= ["GET", "POST"])
def sigtest(debug=True):
    # ------- Get cookies
    recommended_test_reasons = json.loads(request.cookies.get('recommended_test_reasons'))
    fileName = request.cookies.get('fileName')
    # ------- Get form data
    sig_test_name = request.form.get('target_sig_test')
    sig_alpha = request.form.get('significance_level')

    if debug:
        print(' ********* Running /sig_test')
        print('Recommended tests reasons={}'.format(recommended_test_reasons))
        print('Sig_test_name={}, sig_alpha={}'.format(sig_test_name, sig_alpha))

    # ------- Test if 'last_tab' was sent
    last_tab_name_clicked = 'Significance Test' #request.form.get('last_tab_input')
    print("***** LAST TAB (from POST): {}".format(last_tab_name_clicked))

    scores1, scores2 = read_score_file(FOLDER + "/" + fileName)  # todo: different FOLDER for session/user
    score_dif = calc_score_diff(scores1, scores2)
    if debug: print("THE SCORE_DIF:{}".format(score_dif))
    test_stat_val, pval, rejection = run_sig_test(sig_test_name, # 't'
                                              score_dif,
                                              float(sig_alpha), #0.05,
                                              B=500) # todo: B_boot
    if debug: print("test_stat_val={}, pval={}, rejection={}".format(test_stat_val, pval, rejection))

    recommended_tests = json.loads(request.cookies.get('recommended_tests'))
    summary_stats_dict = json.loads(request.cookies.get('summary_stats_dict'))
    rendered = render_template(template_filename,
                               # specific to effect size test
                               effect_size_estimators=estimators,
                               eff_estimator=request.cookies.get('eff_estimator'),
                               eff_size_val=request.cookies.get('eff_size_val'),
                               help1 = helper("function 1"),
                               help2 = helper("function 2"),
                               #file_uploaded = "File uploaded!!: {}".format(fileName),
                               last_tab_name_clicked= last_tab_name_clicked,
                           # get from cookies
                           eval_unit_size=request.cookies.get('eval_unit_size'),
                           eval_unit_stat=request.cookies.get('eval_unit_stat'),
                           shuffle_seed=request.cookies.get('shuffle_seed'),
                           sigtest_heading=request.cookies.get('sig_test_heading'), # todo: add teststat_heading
                           summary_str=request.cookies.get('summary_str'),
                           mean_or_median = request.cookies.get('mean_or_median'),
                           is_normal = request.cookies.get('is_normal'),
                               recommended_tests = recommended_tests,
                               recommended_tests_reasons = recommended_test_reasons,
                               summary_stats_dict = summary_stats_dict,
                               hist_score1=request.cookies.get('hist_score1'),
                               hist_score2=request.cookies.get('hist_score2'),
                               hist_diff=request.cookies.get('hist_diff'),
                               hist_diff_par=request.cookies.get('hist_diff_par'),
                           # specific to sig_test
                               sig_test_stat_val = test_stat_val,
                               pval = pval,
                               rejectH0 = rejection,
                               sig_alpha = sig_alpha,
                               sig_test_name = sig_test_name
                               )
    resp = make_response(rendered)
    # -------- WRITE TO COOKIES ----------
    resp.set_cookie('sig_test_name', sig_test_name)
    resp.set_cookie('sig_test_alpha', sig_alpha)
    resp.set_cookie('sig_test_stat_val', json.dumps(test_stat_val) )
    print('test_stat_val={}, json_dumped={}'.format(test_stat_val, json.dumps(test_stat_val)))
    resp.set_cookie('pval', str(pval))
    resp.set_cookie('rejectH0', str(rejection))
    return resp

@app.route('/effectsize', methods= ["GET", "POST"])
def effectsize():
    if request.method == 'POST':
        last_tab_name_clicked = 'Effect Size'
        fileName = request.cookies.get('fileName')
        scores1, scores2 = read_score_file(FOLDER + "/" + fileName) # todo: different FOLDER for session/user
        # get dif
        score_dif = calc_score_diff(scores1, scores2)

        previous_selected_est = request.cookies.get('eff_estimator')

        # todo: check if different from previous
        cur_selected_est = request.form.get('target_eff_test')

        print('previous estimator={}, current estimator={}'.format(
            previous_selected_est , cur_selected_est))

        # old:
        # (estimates, estimators) = calc_eff_size(cur_selected_test,
        #                                         effect_size_target_stat,
        #                                         score_dif)
        # print('Estimates: {}\nEstimators: {}'.format(estimates, estimators))
        # if len(estimators) != len(estimates):
        #     print("Warning (effect size): {} estimators but {} estimates".format(
        #         len(estimators), len(estimates)
        #     ))


        eff_size_val = calc_eff_size(cur_selected_est, score_dif)

        # For completing previous tabs: target_stat is 'mean' or 'median'
        previous_selected_test = request.cookies.get('sig_test_name')
        recommended_test_reasons = json.loads(request.cookies.get('recommended_test_reasons'))
        recommended_tests = json.loads(request.cookies.get('recommended_tests'))
        summary_stats_dict = json.loads(request.cookies.get('summary_stats_dict'))
        rendered = render_template(template_filename,
                                   # specific to effect size test
                                   effect_size_estimators = estimators,
                                   eff_estimator = cur_selected_est,
                                   eff_size_val = eff_size_val,
                                   #effect_size_estimates = estimates,
                                   #effect_estimator_dict = est_dict,
                                   help1=helper("function 1"),
                                   help2=helper("function 2"),
                                   # file_uploaded = "File uploaded!!: {}".format(fileName),
                                   last_tab_name_clicked=last_tab_name_clicked,
                                   # get from cookies
                                   eval_unit_size=request.cookies.get('eval_unit_size'),
                                   eval_unit_stat=request.cookies.get('eval_unit_stat'),
                                   shuffle_seed=request.cookies.get('shuffle_seed'),
                                   sigtest_heading=request.cookies.get('sig_test_heading'), # todo: add teststat_heading
                                   summary_str=request.cookies.get('summary_str'),
                                   mean_or_median=request.cookies.get('mean_or_median'),
                                   is_normal=request.cookies.get('is_normal'),
                                   recommended_tests=recommended_tests,
                                   recommended_tests_reasons=recommended_test_reasons,
                                   summary_stats_dict=summary_stats_dict,
                                   hist_score1=request.cookies.get('hist_score1'),
                                   hist_score2=request.cookies.get('hist_score2'),
                                   hist_diff=request.cookies.get('hist_diff'),
                                   hist_diff_par=request.cookies.get('hist_diff_par'),
                                   # specific to sig_test
                                   sig_test_stat_val=request.cookies.get('sig_test_stat_val'), # json.loads?
                                   pval=request.cookies.get('pval'),
                                   rejectH0=request.cookies.get('rejectH0'),
                                   sig_alpha=request.cookies.get('sig_test_alpha'),
                                   sig_test_name=request.cookies.get('sig_test_name')
                                   )

        resp = make_response(rendered)
        # -------- WRITE TO COOKIES ----------
        resp.set_cookie('effect_estimator_dict',json.dumps(estimators))
        if cur_selected_est:
            resp.set_cookie('eff_estimator', cur_selected_est)
        if eff_size_val:
            resp.set_cookie('eff_size_val', str(eff_size_val))
        return resp

    elif request.method == 'GET':
        # You got to the main page by navigating to the URL, not by clicking submit
            #full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
            #full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
        return render_template('tab_interface.html')

@app.route('/power', methods= ["GET", "POST"])
def power():
    last_tab_name_clicked = 'Post-test Power Analysis'
    fileName = request.cookies.get('fileName')
    scores1, scores2 = read_score_file(FOLDER + "/" + fileName)  # todo: different FOLDER for session/user
    # get dif
    score_dif = calc_score_diff(scores1, scores2)
    step_size = 40  #todo: get from form
    pow_sampsizes = post_power_analysis('sig_test_name', 'montecarlo', score_dif, step_size,
                        output_dir=FOLDER)
    print(pow_sampsizes)
    power_file = 'power_samplesizes.svg'
    power_path = os.path.join(app.config['FOLDER'], power_file)


    recommended_test_reasons = json.loads(request.cookies.get('recommended_test_reasons'))
    recommended_tests = json.loads(request.cookies.get('recommended_tests'))
    summary_stats_dict = json.loads(request.cookies.get('summary_stats_dict'))
    rendered = render_template(template_filename,
                               # specific to effect size test
                               effect_size_estimators=estimators,
                               eff_estimator=request.cookies.get('eff_estimator'),
                               eff_size_val=request.cookies.get('eff_size_val'),
                               # effect_size_estimates = estimates,
                               # effect_estimator_dict = est_dict,
                               help1=helper("function 1"),
                               help2=helper("function 2"),
                               # file_uploaded = "File uploaded!!: {}".format(fileName),
                               last_tab_name_clicked=last_tab_name_clicked,
                               # get from cookies
                               eval_unit_size=request.cookies.get('eval_unit_size'),
                               eval_unit_stat=request.cookies.get('eval_unit_stat'),
                               shuffle_seed=request.cookies.get('shuffle_seed'),
                               sigtest_heading=request.cookies.get('sig_test_heading'),  # todo: add teststat_heading
                               summary_str=request.cookies.get('summary_str'),
                               mean_or_median=request.cookies.get('mean_or_median'),
                               is_normal=request.cookies.get('is_normal'),
                               recommended_tests=recommended_tests,
                               recommended_tests_reasons=recommended_test_reasons,
                               summary_stats_dict=summary_stats_dict,
                               hist_score1=request.cookies.get('hist_score1'),
                               hist_score2=request.cookies.get('hist_score2'),
                               hist_diff=request.cookies.get('hist_diff'),
                               hist_diff_par=request.cookies.get('hist_diff_par'),
                               # specific to sig_test
                               sig_test_stat_val=request.cookies.get('sig_test_stat_val'),  # json.loads?
                               pval=request.cookies.get('pval'),
                               rejectH0=request.cookies.get('rejectH0'),
                               sig_alpha=request.cookies.get('sig_test_alpha'),
                               sig_test_name=request.cookies.get('sig_test_name'),
                               # power
                               power_file = power_path
                               )

    resp = make_response(rendered)
    # -------- WRITE TO COOKIES ----------
    # resp.set_cookie('pow_sampsizes', json.dumps(pow_sampsizes))
    return resp


# https://www.roytuts.com/how-to-download-file-using-python-flask/
@app.route('/download')
def download_file():
        os.system("zip -r user/r.zip user/*")
        path = "user/r.zip"
        return send_file(path, as_attachment=True)

@app.route('/img_url/<image_path>')
def send_img_file(image_path, debug=True):
    '''
    if the file path is known to be a relative path then alternatively:
        return send_from_directory(dir_name, image_name)
    @param image_path: The full path to the image
    @param debug: print out the path
    @return:
    '''
    if debug: print('display image: {}'.format(image_path))
    return send_file(image_path)

# --- End examples ----

if __name__ == "__main__":
    app.debug=True
    app.run()
