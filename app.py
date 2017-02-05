from flask import Flask
from flask import render_template, request, redirect
app = Flask(__name__)
from flask import request, send_file
import pdb
import intersect
import tempfile


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        with tempfile.NamedTemporaryFile() as people_file:
            request.files["people"].save(people_file.name)
            people = intersect.people_df(people_file.name)

            with tempfile.NamedTemporaryFile() as shapes_file:
                request.files["shapes"].save(shapes_file.name)
                shapes = intersect.shapes_df(shapes_file.name)

                print("Merging...")
                merged = intersect.merge(shapes, people)

                with tempfile.NamedTemporaryFile() as merged_file:
                    print("Converting to CSV...")
                    merged.to_csv(merged_file.name)
                    return send_file(merged_file.name, mimetype='text/csv')

    if request.method == "GET":
        return render_template('index.html')


@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run()
