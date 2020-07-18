from flask import *
from flask import render_template
from data_analysis import read_score_file, plot_hist
import os

FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['FOLDER'] = FOLDER

@app.route('/', methods= ["GET", "POST"])
def homepage():
    if request.method == 'POST':

        scores1, scores2 = read_score_file("score")
        plot_hist(scores1, scores2)

        eval_unit_size = request.form.get('eval_unit_size')
        seed = request.form.get('seed')

        if seed and eval_unit_size:
            result = 'Your results are displayed below. '\
                   + '; Seed is: ' + seed \
                   + "; Evaluation unit is: " + eval_unit_size
            return jsonify(result=result)
        else:
            return jsonify(result='Input needed for more details.')

    full_filename1 = os.path.join(app.config['FOLDER'], 'hist_score1.svg')
    full_filename2 = os.path.join(app.config['FOLDER'], 'hist_score2.svg')
    return render_template('da.html',
                           hist_score1 = full_filename1,
                           hist_score2 = full_filename2)

if __name__ == "__main__":
    app.debug=True
    app.run()
