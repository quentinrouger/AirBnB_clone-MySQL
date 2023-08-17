#!/usr/bin/python3

"""This is a script thats starts a Flask web application"""


from flask import Flask

blog_app = Flask(__name__)


@blog_app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

if __name__ == "__main__":
    blog_app.run(host="0.0.0.0", port=5000)
