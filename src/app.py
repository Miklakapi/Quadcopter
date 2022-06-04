"""This module manages the web server."""

import os
from flask import Flask, send_from_directory, render_template, request


app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/direction/<action>')
def direction(action):
    ### TODO ###
    print(action)
    return '', 200


@app.route('/power/<strength>')
def power(strength):
    ### TODO ###
    print(strength)
    return '', 200


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
