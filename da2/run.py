# v2 - using tabs
from flask import *
from flask import render_template
from data_analysis import read_score_file, plot_hist, calc_score_diff, plot_hist_diff, partition_score, skew_test
from effectSize import calc_eff_size
from help import helper
from werkzeug.utils import secure_filename
import os
import numpy as np

FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['FOLDER'] = FOLDER

# defaults
DEFAULT_SEED = None
DEFAULT_EVAL_SIZE = 1

@app.route('/', methods= ["GET", "POST"])
def homepage():
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

        # skewness test
        mean_or_median = skew_test(score_diff_par)

        if eval_unit_size:
            result_str = 'Your results are displayed below. Based on skewness, you should use {} as the test statistic.\nSeed = {} Eval unit size = {}'.format(
                mean_or_median,
                seed,
                eval_unit_size)
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
                rendered = render_template('tab_interface.html',
                                       file_uploaded = "File uploaded.",
                                       result_str = result_str,
                                       hist_score1=full_filename1,
                                       hist_score2=full_filename2,
                                       hist_diff= full_filename_dif,
                                       hist_diff_par= full_filename_dif_par)
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
                               file_uploaded = "Upload a file.")


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
