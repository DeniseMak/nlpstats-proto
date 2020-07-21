# v2 - using tabs
from flask import *
from flask import render_template
from data_analysis import read_score_file, plot_hist
from werkzeug.utils import secure_filename
import os

FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['FOLDER'] = FOLDER

@app.route('/', methods= ["GET", "POST"])
def homepage():
    if request.method == 'POST':
        f = request.files['system_file']  # new
        f.save(secure_filename(f.filename))  # todo: change this to 'uploads' directory

        scores1, scores2 = read_score_file(f.filename) #read_score_file("score")
        plot_hist(scores1, scores2)

        eval_unit_size = request.form.get('eval_unit_size')
        seed = request.form.get('seed')



        if seed and eval_unit_size:
            result_str = 'Your results are displayed below. '\
                   + '; Seed is: ' + seed \
                   + "; Evaluation unit is: " + eval_unit_size
            # new
            full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
            full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
            input_filename_str =  "input_filename was: " + f.filename
            print(input_filename_str)

            rendered = render_template('tab_interface.html',
                                       result_str=result_str,
                                       hist_score1=full_filename1,
                                       hist_score2=full_filename2) #result1=dicts[0], result2=dicts[1])
            return rendered #return jsonify(result=result_str, filename=input_filename)
        else:
            return jsonify(result='Input needed for more details.')
    elif request.method == 'GET':
        #full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
        #full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
        return render_template('tab_interface.html')
        '''
        return render_template('tab_interface.html',
                               hist_score1 = full_filename1,
                               hist_score2 = full_filename2) 
                               '''

if __name__ == "__main__":
    app.debug=True
    app.run()
