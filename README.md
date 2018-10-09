# STREAM ONLINE VIEWER

**STREAM ONLINE VIEWER** is an application to allow multiple clients to display a live stream and visualize it on a web client via browser.

### Definition
-   Multiple clients can watch the stream on one web server (multiple web clients connected).
- The server should be always listening to the stream for messages and discard this messages if there are no clients to send the message to.
- Each client should start receiving images from the moment he connects onward (do not send old images that the server received before the client connected).
- When a user opens the web page, it should automatically start receiving the latest data from the server. The web page should display to the user the image and metadata from the stream.

### Architecture & Technology stack
Angular + Python + Flask

- Angular is JavaScript (well, actually written in Typescript) framework for building Single Page Application.
- Python is server side programming language and very powerful to build complex IoT, Image Processing and other types of system.
- Flask is a REST API framework for Python.

For communication between server and clients, Flask-SocketIO(https://flask-socketio.readthedocs.io/en/latest/) has been used. It gives low latency bi-directional communications between the clients and the server.

For the front end design, Materialize(https://materializecss.com/) was used. It is a modern responsive front-end framework based on Material Design (https://material.io/), developed by Google.


## Installation
To install the STREAM ONLINE VIEWER clone the repository and set up the anaconda virtual environment based on the requirements.txt file in combination with pip and virtualenv.

```bash
git clone https://github.com/lhdamiani/interview_stream_online_viewer
cd interview_stream_online_viewer
mkvirtualenv -p /usr/local/anaconda3/bin/python interview
pip install -r requirements.txt 
```
> **Note**: if mkvirtualenv is not found, make sure to set the environment variable VIRTUALENVWRAPPER_PYTHONto pointing to `export VIRTUALENVWRAPPER_PYTHON=/usr/local/anaconda3/bin/python`


### Dependencies
In order to use this repository, you will have to install the following conda packages:

- matplotlib
- numpy
- bsread

You can do this (on Linux) by running:
```bash
conda install -c paulscherrerinstitute bsread numpy matplotlib
```

When installing PSI libraries you have to specify that you want to install them from the PSI Anaconda repository (the "-c paulscherrerinstitute" flag in the command above).

> **Note**: if conda is not found, make sure to add to the path `export PATH=/Users/lhdamiani/miniconda3/bin:$PATH`, don't forget to change the username.

## Run
-------------------------
To run the Flask-Socketio web server from the ROOT folder:

```bash
export PYTHONPATH=$(pwd):${PYTHONPATH}
python stream_online_viewer/start_server.py -H <HOST> -P <PORT> -S <SOURCE_STREAM_PORT> -O <SOURCE_STREAM_HOST>
```
> **Note**: Default values for `<HOST>`, `<PORT>`, `<SOURCE_STREAM_PORT>` and `<SOURCE_STREAM_HOST>` are 127.0.0.1, 5000, 8888, and 127.0.0.1 respectively.

To run the data generator:
```bash
export PYTHONPATH=$(pwd):${PYTHONPATH}
python stream_online_viewer/start_stream.py
```
> **Note**: Default values for the data generated is 8888

To access the client viewer go to 127.0.0.1:5000 on your browser
> **Note**: Firefox is recommended.

and proceed with the login

**Username: admin**

**Password: password**

> **Note**: For the purpose of this task, not much effort has been invested into the security method. The method adopted simply serves as a reminder that such web app needs security.

The client works in any screen-width - it is ready for mobile usage and small screens.

### Data stream generator

This is the protocol we use to transfer beam synchronous data at SwissFEL: [https://github.com/paulscherrerinstitute/bsread_python](https://github.com/paulscherrerinstitute/bsread_python)

> **Note:** You will not be able to access the real BSread stream from outside of PSI. This repository has a stream generator you can use to simulate camera images and metadata you will later display to the clients. 


The generator is located in **stream_online_viewer/start_stream.py** and can be run from the ROOT of this repository:
```
export PYTHONPATH=$(pwd):${PYTHONPATH}
python stream_online_viewer/start_stream.py
```


### Possible improvements and drawbacks

|What?|Current implementation|How to improve?|
|----------------|-------------------------------|-----------------------------|
|Performance| Due to time and purpose of this task, the focus was to implement a minimally running example with the desired functionality. Flask-SocketIO was used to communication between server and clients. Analysis and benchmarks analysing the performance of Flask-SocketIO have been performed by others and provide a satisfactory results for this application. Such analysis can be found in http://drewww.github.io/socket.io-benchmarking/ and http://blog.mixu.net/2011/11/22/performance-benchmarking-socket-io-0-8-7-0-7-11-and-0-6-17-and-nodes-native-tcp/| Deeper analysis about possible tools can be further analyzed once the time is not a constraint. |
|Security|Just a simple login/password to block the visualization of the web app contet.| Implementation of security using Flask-Security(https://pythonhosted.org/Flask-Security/) or Flask-Oauth(https://pythonhosted.org/Flask-OAuth/)|
|Image loading|For this tasks purpose, the web server receives the message from the data stream generator and saves it to a local file image which is refreshed on the client side's browser. Probably with a high rate of messages it could be a problem to show them with a high frequency. |Transmission of the image data by some encoding protocol which would transfer the data it on a more efficient way without the cost of writing to a disk and re-loading on the client's side. Encoding/Decoding protocols as B64 could be of use https://www.base64-image.de/.|
|Mobile access and different browsers| Current implementation was focused on regular computer 'width' screens but implemented with angular and materialize which allows small screens to access the content in a responsive way. But, due to the time constraint and purpose of this task, no extensive tests have been made in order to assure that all functionalities are flawless. Firefox browser was used for development.| Perform tests and evaluate the usability and functionalities on small-screens devices and different browsers.|


### Acknowledgement

This application was loosely developed based on this repository: https://github.com/miguelgrinberg/Flask-SocketIO


### Changelog

See file `CHANGES.rst`.

## Contact

For comments, contact:
```
leonardo.hax@psi.ch
```