from flask import Flask, url_for, redirect, request, render_template, make_response
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
import sig_test_procedures.data_analysis as data


@app.route('/uploader2', methods=['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file1']
      f2 = request.files['file2']
      f2.save(secure_filename(f2.filename))
      f.save(secure_filename(f.filename))  # todo: change this to 'uploads' directory

      dicts = data.read_score_file(f.filename)
      rendered = render_template('da_temp.html', result1=dicts[0], result2=dicts[1])
      return rendered

if __name__ == '__main__':
   app.run(debug = True)
