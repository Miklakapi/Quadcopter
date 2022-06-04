"""This module manages the web visualizer."""

import os
from flask import Flask, send_from_directory, render_template

import import_from_root


app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-data')
def get_data():
    return {'1': 10, '2': 5, '3': 2, '4': 1}


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
