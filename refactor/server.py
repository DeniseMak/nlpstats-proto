from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


def get_rand_state_str():
    '''
    This is a random string that's generate every time a 'submit' operation happens.
    It's used to distinguish when the state of the app may have changed.
    @return: A random int between 0 and 9999
    '''
    rand_str = str(np.random.randint(10000))
    return rand_str


@app.route('/json')
def json():
    return render_template('interface2.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")
