from flask import Flask
from flask import render_template
app = Flask(__name__)

import pdb

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')
