from flask import Flask, url_for, redirect, request, render_template, make_response
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
   # list files in this directory
   dir = 'pictures'
   files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
   return render_template('list_files.html', file_list = files)


@app.route('/upload')
def upload_page():
   return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      if not user:
         user = 'Foo'
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      if not user:
         user = 'Anonymous'
      return redirect(url_for('success',name = user))

@app.route('/')
def index():
   #return redirect(url_for('hello_world', name='Dude'))
   # return redirect(url_for('hello', name='Dude'))
   return render_template('index.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
      user = request.form['nm']

   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('userID', user)
   return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'

#@app.route('/hello/<name>/')  # if a user visits '/', the output of the hello_world() function is rendered in the browser
def hello_world(name):
   #return 'Hello {}!!!'.format(name)
   dict = {'phy': 50, 'che': 60, 'maths': 70}
   return render_template('hello.html', name = name, result = dict)

app.add_url_rule('/hello/<name>/', 'hello', hello_world)

def hello_1():
   return 'Hello 1.'
app.add_url_rule('/hello1', 'hello1', hello_1)

if __name__ == '__main__':
   app.run(debug = True)
