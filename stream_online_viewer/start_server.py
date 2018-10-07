
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask_restful import Resource, Api
from flask_material import Material  
from flask_cors import CORS
from flask import Flask, flash, jsonify, render_template, url_for, copy_current_request_context, request, make_response, session, redirect, abort, _request_ctx_stack
from threading import Thread, Event
import optparse
from bsread import source
from matplotlib import pyplot, image

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



class ClientThread(Thread):
    def __init__(self, port, n_img, stream_host):
        super(ClientThread, self).__init__()
        self._delay = 1.5
        self._stream_output_port = port
        self._n_images = n_img
        self._stream_host = stream_host

    def receive_stream(self):
        """Function that receives the stream and send the signal for the clients using socketio.

            """
        message = None

        # You always need to specify the host parameter, otherwise bsread will try to access PSI servers.
        with source(host=self._stream_host, port=self._stream_output_port, receive_timeout=1000) as input_stream:

            n_received = 0
            # Detects how many messages are expected
            if self._n_images == -1:
                while True:
                    message = input_stream.receive()
                    # In case of receive timeout (1000 ms in this example), the received data is None.
                    if message is None:
                        continue
                    else:
                        # Creates the image and saves to the file that is shown to the client
                        pyplot.imshow(message.data.data['image'].value)
                        pyplot.savefig('./stream_online_viewer/static/images/stream.png')
                        # Increases the number of received messages
                        n_received += 1
                        # Generates the data containing meaningful information to the client
                        data = {'number_of_received_messages':  n_received, 
                                'data': n_received,
                                'messages_received': float(message.statistics.messages_received),
                                'total_bytes_received': float(message.statistics.total_bytes_received),
                                'repetition_rate': float(message.data.data['repetition_rate'].value),
                                'beam_energy': float(message.data.data['beam_energy'].value),
                                'image_size_y': float(message.data.data['image_size_y'].value),
                                'image_size_x': float(message.data.data['image_size_x'].value)
                                }
                        # emits the signal with the data
                        socketio.emit('newmessage', data, namespace='/test')
            else:
                for _ in range(self._n_images):
                    message = input_stream.receive()
                    # In case of receive timeout (1000 ms in this example), the received data is None.
                    if message is None:
                        continue
                    else:
                        # Creates the image and saves to the file that is shown to the client
                        pyplot.imshow(message.data.data['image'].value)
                        pyplot.savefig('./stream_online_viewer/static/images/stream.png')
                        # Increases the number of received messages
                        n_received += 1
                        # Generates the data containing meaningful information to the client
                        data = {'number_of_received_messages':  n_received, 
                                'data': n_received,
                                'messages_received': float(message.statistics.messages_received),
                                'total_bytes_received': float(message.statistics.total_bytes_received),
                                'repetition_rate': float(message.data.data['repetition_rate'].value),
                                'beam_energy': float(message.data.data['beam_energy'].value),
                                'image_size_y': float(message.data.data['image_size_y'].value),
                                'image_size_x': float(message.data.data['image_size_x'].value)
                                }
                        # emits the signal with the data
                        socketio.emit('newmessage', data, namespace='/test')

    def run(self):
        self.receive_stream()
        

# Handles the 404 error and renders the 404 template.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Detects a new client connected and start the thread.
@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = ClientThread(int(default_port_source), -1, default_host_source)
        thread.start()

# Detecs when a client disconnects
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

# RESTFUL API for index
class Index(Resource):
    def __init__(self):
        pass
    def get(self):
        headers = {'Content-Type': 'text/html'}
        # allows the visualization of index if session logged in
        if not session.get('logged_in'):
            return make_response(render_template('login.html'), 200, headers)
        else:
            return make_response(render_template('index.html'), 200, headers)

# RESTFUL API for login
class Login(Resource):
    def __init__(self):
        pass
    def post(self):
        headers = {'Content-Type': 'text/html'}
        # Detects if the username/password are correct and starts the session
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return make_response(render_template('index.html'), 200, headers)
        else:    
            flash("Try again...")
            return make_response(render_template('login.html'), 200, headers)

# RESTFUL API for logout
class Logout(Resource):
    def __init__(self):
        pass
    def get(self):
        session['logged_in'] = False
        return redirect(url_for('index'))

# Adds all the restful apis resources
api.add_resource(Index, '/')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')

if __name__ == '__main__':
    # Default host 
    default_host="127.0.0.1"
    # Default port
    default_port="5000"
    # Default host stream
    default_host_source="localhost"
    # Default port stream
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
    
    parser.add_option("-O", "--source_host",
        help="host for the source generator " + \
            "[default %s]" % default_host_source,
        default=default_host_source)

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
