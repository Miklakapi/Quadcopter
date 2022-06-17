"""This module manages the web server."""

import os
from flask import Flask, send_from_directory, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import multiprocessing


try:
    from quadcopter import Quadcopter

    powers = multiprocessing.Manager().list()
    powers.append(0)

    drone = Quadcopter(multiprocessing.Manager().Queue(), powers)
    drone.start(test=True)
except Exception as error:
    print(error)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


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
    try:
        socketio.run(app, host='0.0.0.0', debug=True, use_reloader=False)
    except KeyboardInterrupt:
        drone.terminate()
        drone.join()
