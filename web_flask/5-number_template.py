#!/usr/bin/python3

"""This is a script thats starts a Flask web application"""


from flask import Flask, render_template

blog_app = Flask(__name__)


@blog_app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@blog_app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@blog_app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    text = text.replace("_", " ")
    return "C " + text


@blog_app.route("/python/", strict_slashes=False)
@blog_app.route("/python/<text>", strict_slashes=False)
def python_text(text="is cool"):
    text = text.replace("_", " ")
    return "Python " + text


@blog_app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    return f"{n} is a number"


@blog_app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)

if __name__ == "__main__":
    blog_app.run(host='0.0.0.0', port='5000')
