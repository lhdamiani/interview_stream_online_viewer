
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask_restful import Resource, Api
from flask_material import Material  
from flask_cors import CORS
from flask import Flask, flash, jsonify, render_template, url_for, copy_current_request_context, request, make_response, session, redirect, abort, _request_ctx_stack
from random import random
from time import sleep
from threading import Thread, Event
from functools import wraps
import os, json, optparse, codecs
from bsread import source
from matplotlib import pyplot, image
import matplotlib
import msgpack
import msgpack_numpy as m
import base64


__author__ = 'hax_damiani'

app = Flask(__name__)
Material(app)
CORS(app)

api = Api(app)
app.config['SECRET_KEY'] = 'HaxDamiani!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)
#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self, port, n_img):
        self._delay = 1.5
        super(RandomThread, self).__init__()
        self._stream_output_port = port
        self._n_images = n_img

    def receive_stream(self):
        """
        to be described
        """
        message = None

        # You always need to specify the host parameter, otherwise bsread will try to access PSI servers.
        with source(host="localhost", port=self._stream_output_port, receive_timeout=1000) as input_stream:

            n_received = 1

            if self._n_images == -1:
                while True:
                    message = input_stream.receive()
                    # In case of receive timeout (1000 ms in this example), the received data is None.
                    if message is None:
                        continue
                    else:
                        pyplot.imshow(message.data.data['image'].value)
                        pyplot.savefig('./stream_online_viewer/static/images/stream.png')

                        n_received += 1
                        data = {'number_of_received_messages':  n_received, 
                                'data': n_received,
                                'messages_received': float(message.statistics.messages_received),
                                'total_bytes_received': float(message.statistics.total_bytes_received),
                                'repetition_rate': float(message.data.data['repetition_rate'].value),
                                'beam_energy': float(message.data.data['beam_energy'].value),
                                # 'image_profile_y': json.dumps(message.data.data['image_profile_y'].value.tolist()),
                                # 'image_profile_x': json.dumps(message.data.data['image_profile_x'].value.tolist()),
                                'image_size_y': float(message.data.data['image_size_y'].value),
                                'image_size_x': float(message.data.data['image_size_x'].value)
                                }
                        socketio.emit('newnumber', data, namespace='/test')
                        
                        
                        
            else:
                for _ in range(self._n_images):
                    message = input_stream.receive()

                    # In case of receive timeout (1000 ms in this example), the received data is None.
                    if message is None:
                        continue

                    n_received += 1
                    print("Number of received images:",n_received)

    def run(self):
        self.receive_stream()
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread(int(default_port_source), -1)
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

class Index(Resource):
    def __init__(self):
        pass
    def get(self):
        headers = {'Content-Type': 'text/html'}
        if not session.get('logged_in'):
            return make_response(render_template('login.html'), 200, headers)
        else:
            return make_response(render_template('index.html'), 200, headers)

class Login(Resource):
    def __init__(self):
        pass
    def post(self):
        headers = {'Content-Type': 'text/html'}
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return make_response(render_template('index.html'), 200, headers)
        else:
            flash("Try again...")
            return make_response(render_template('login.html'), 200, headers)

class Logout(Resource):
    def __init__(self):
        pass
    def get(self):
        session['logged_in'] = False
        return redirect(url_for('index'))

api.add_resource(Index, '/')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')

if __name__ == '__main__':
    # Default host 
    default_host="127.0.0.1"
    # Default port
    default_port="5000"

    # Default port
    default_port_source="8888"
    # Parser of the options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
        help="Hostname of the Flask app " + \
            "[default %s]" % default_host,
        default=default_host)
    parser.add_option("-P", "--port",
        help="Port for the Flask app " + \
            "[default %s]" % default_port,
        default=default_port)
    
    parser.add_option("-S", "--source_port",
        help="Port for the source generator " + \
            "[default %s]" % default_port_source,
        default=default_port_source)

    parser.add_option("-d", "--debug",
        action="store_true", dest="debug",
        help=optparse.SUPPRESS_HELP)
    options, _ = parser.parse_args()

    socketio.run(app,
        debug=options.debug,
        host=options.host,
        port=int(options.port))
