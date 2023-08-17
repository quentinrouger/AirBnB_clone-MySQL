#!/usr/bin/python3

"""This is a script thats starts a Flask web applications"""

from models import storage
from models.state import State
from flask import Flask, render_template

blog_app = Flask(__name__)


@blog_app.route('/states_list', strict_slashes=False)
def states_list():
    return render_template('7-states_list.html', states_li=storage.all(State))


@blog_app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    return render_template("/8-cities_by_states.html", sts=storage.all(State))


@blog_app.teardown_appcontext
def tear_down(self):
    storage.close()

if __name__ == "__main__":
    blog_app.run(host='0.0.0.0', port='5000')
