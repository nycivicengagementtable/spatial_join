from flask import Flask
from flask import render_template
app = Flask(__name__)
from flask import request
import pdb


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        people, shapes = request.files["people"].read(), request.files["shapes"].read()
        pdb.set_trace()
        # f = request.files['the_file']
        f.save('/var/www/uploads/')
    if request.method == "GET":
        return render_template('index.html')


@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run()
