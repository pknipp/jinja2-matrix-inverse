import cmath
from flask import Flask, render_template
from . import helper

app = Flask(__name__)

# The following are used to wrap the html string created for server-side rendering.
top = "<head><title>Matrix inverse</title></head><body>"
bottom = "<p align=center>creator:&nbsp;<a href='https://pknipp.github.io/' target='_blank' rel='noopener noreferrer'>Peter Knipp</a><br/>repo:&nbsp;<a href='https://github.com/pknipp/matrix-inverse' target='_blank'  rel='noopener noreferrer'>github.com/pknipp/matrix-inverse</a></p></body>"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/<square_in>')
def square(square_in):
    results = helper.parse(False, square_in)
    if "error" in results:
        return render_template('error.html', message=results["error"]["message"], strings=results["error"]["strings"])
    else:
        determinant = results["determinant"]
        original_matrix = results["original matrix"]
        n = len(original_matrix)
        original_matrix = enumerate(original_matrix)
        inhomogeneous_part=results["inhomogeneous part"]
        m = len(inhomogeneous_part)
        solutions = results["solutions"]
        inverse_matrix = results.get("inverse matrix")
        warning = results.get("warning")
        if inverse_matrix is not None:
            inverse_matrix = enumerate(inverse_matrix)
        return render_template("results.html", determinant=determinant, n=n, m=m, original_matrix=original_matrix, inhomogeneous_part=inhomogeneous_part, inverse_matrix=inverse_matrix, solutions=solutions, warning=warning)

@app.route('/<square_in>/<rect_in>')
def rect(square_in, rect_in):
    results = helper.parse(False, square_in, rect_in)
    if "error" in results:
        return render_template('error.html', message=results["error"]["message"], strings=results["error"]["strings"])
    else:
        determinant = results["determinant"]
        original_matrix = results["original matrix"]
        n = len(original_matrix)
        original_matrix = enumerate(original_matrix)
        inhomogeneous_part=results["inhomogeneous part"]
        m = len(inhomogeneous_part)
        solutions = results["solutions"]
        inverse_matrix = results.get("inverse matrix")
        warning = results.get("warning")
        if inverse_matrix is not None:
            inverse_matrix = enumerate(inverse_matrix)
        return render_template("results.html", determinant=determinant, n=n, m=m, original_matrix=original_matrix, inhomogeneous_part=inhomogeneous_part, inverse_matrix=inverse_matrix, solutions=solutions, warning=warning)

@app.route('/json/<square_in>')
def json_square(square_in):
    return helper.parse(True, square_in)

@app.route('/json/<square_in>/<rect_in>')
def json_rect(square_in, rect_in):
    return helper.parse(True, square_in, rect_in)
