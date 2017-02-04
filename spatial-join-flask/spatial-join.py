from flask import Flask
from flask import render_template, request, redirect
app = Flask(__name__)
import pdb


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        people, shapes = request.files["people"].read(), request.files["shapes"].read()
        # people.save('/var/www/uploads/')
        return redirect("/results")
    if request.method == "GET":
        return render_template('index.html')


@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run()
