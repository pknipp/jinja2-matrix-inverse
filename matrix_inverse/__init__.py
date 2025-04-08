import cmath
from flask import Flask, render_template
from . import helper

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')

@app.route('/')
def hello():
    return render_template(
        'index.html',
        base_url="https://matrix-inverse.herokuapp.com",
        frag1 = "/[[1,2],[3,4]]",
        frag2 = "/[[1,2],[3,4]]/[[3,5],[2,4],[-1,0]]",
    )

@app.route('/<square_in>')
def square(square_in):
    results = helper.parse(False, square_in)
    if "error" in results:
        return render_template(
            'error.html',
            message=results["error"]["message"],
            strings=results["error"]["strings"],
        )
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

@app.route('/api/<square_in>')
def json_square(square_in):
    return helper.parse(True, square_in)

@app.route('/api/<square_in>/<rect_in>')
def json_rect(square_in, rect_in):
    return helper.parse(True, square_in, rect_in)
