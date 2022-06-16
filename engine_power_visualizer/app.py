"""This module manages the web visualizer."""

import os
import logging
from time import sleep
from flask import Flask, send_from_directory, render_template, Response
import multiprocessing
from flask_cors import CORS

import import_from_root
from src.quadcopter import Quadcopter


data = multiprocessing.Manager().list()
data.append(0)
app = Flask(__name__)
CORS(app)
drone = Quadcopter()


def run_quadcopter(variable):
    try:
        while True:
            drone.run()
            variable[0] = drone.get_powers()
            sleep(0.1)
    except KeyboardInterrupt:
        return


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-data')
def get_data():
    return data[0]


@app.route('/power/<power>')
def set_main_power(power: float):
    return Response(status=200)


if __name__ == '__main__':
    proccess = multiprocessing.Process(target=run_quadcopter, args=(data,))
    # logging.getLogger('werkzeug').disabled = True
    try:
        proccess.start()
        app.run('0.0.0.0', debug=True)
    except KeyboardInterrupt:
        proccess.terminate()
        proccess.join()