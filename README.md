# Flask-Socketio web server

**Flask-Socketio web server** is an application to allow multiple clients to display a live stream and visualize it on a web client via browser.

### Definition
-   Multiple clients can watch the stream on one web server (multiple web clients connected).
- The server should be always listening to the stream for messages and discard this messages if there are no clients to send the message to.
- Each client should start receiving images from the moment he connects onward (do not send old images that the server received before the client connected).
- When a user opens the web page, it should automatically start receiving the latest data from the server. The web page should display to the user the image and metadata from the stream.
### Architecture

### test

|                |Test                          |Test                         |
|----------------|-------------------------------|-----------------------------|
|test|test            |test            |


## Installation
To install the Flask-Socketio web server clone the repository and set up the anaconda virtual environment based on the requirements.txt file in combination with pip and virtualenv.

```bash
git clone https://github.com/lhdamiani/interview_stream_online_viewer
cd interview_stream_online_viewer
mkvirtualenv -p /usr/local/anaconda3/bin/python interview
pip install -r requirements.txt 
```
### Dependencies

We use Anaconda for packaging our libraries. If you are not familiar with Anaconda, have a look at their website:

[https://anaconda.org/](https://anaconda.org/)

In order to use this repository, you will have to install the following conda packages:

-   matplotlib
-   numpy
-   bsread

You can do this (on Linux) by running:

conda install -c paulscherrerinstitute bsread numpy matplotlib

We have our own Anaconda repository: [https://anaconda.org/paulscherrerinstitute/](https://anaconda.org/paulscherrerinstitute/)

When installing PSI libraries you have to specify that you want to install them from the PSI Anaconda repository (the "-c paulscherrerinstitute" flag in the command above).

### Dependencies
In order to use this repository, you will have to install the following conda packages:

- matplotlib
- numpy
- bsread

You can do this (on Linux) by running:
```bash
conda install -c paulscherrerinstitute bsread numpy matplotlib
```

## Run
-------------------------
To run the Flask-Socketio web server from the ROOT folder:

```bash
export PYTHONPATH=$(pwd):${PYTHONPATH}
python stream_online_viewer/start_server.py -H <HOST> -P <PORT> -S <SOURCE_STREAM_PORT>
```
> **Note**: Default values for `<HOST>`, `<PORT>` and `<SOURCE_STREAM_PORT>` are 127.0.0.1, 5000 and 8888, respectively.

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

## Contact

For comments and requests, contact:
```
leonardo.hax@psi.ch
```

### Acknowledgement

This application was developed based on this repository: https://github.com/miguelgrinberg/Flask-SocketIO


### Changelog

See file `CHANGES.rst`.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
