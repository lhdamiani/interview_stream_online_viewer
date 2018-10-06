
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
import os, json, optparse

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
    def __init__(self):
        self.delay = 1.5
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random()*10, 1)
            # print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


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
        thread = RandomThread()
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


# @app.route("/logout")
# def logout():
    # session['logged_in'] = False
    # return redirect(url_for('index'))
    

api.add_resource(Index, '/')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')

if __name__ == '__main__':
    # Default host 
    default_host="127.0.0.1"
    # Default port
    default_port="5000"
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

    parser.add_option("-d", "--debug",
        action="store_true", dest="debug",
        help=optparse.SUPPRESS_HELP)
    options, _ = parser.parse_args()

    socketio.run(app,
        debug=options.debug,
        host=options.host,
        port=int(options.port))
