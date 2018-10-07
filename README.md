# Flask-Socketio web server
-------------------------

Flask-Socketio web server is an application to allow multiple clients to receive a live stream and visualize it on their browser.

This application was developed based on this repository: https://github.com/miguelgrinberg/Flask-SocketIO

## Installation
-------------------------
To install the Flask-Socketio web server clone the repository and set up the anaconda virtual environment based on the requirements.txt file in combination with pip and virtualenv.

```bash
git clone https://github.com/lhdamiani/interview_stream_online_viewer
cd interview_stream_online_viewer
mkvirtualenv -p /usr/local/anaconda3/bin/python interview
cd backend
pip install -r requirements.txt 
```

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
python stream_online_viewer/start_server.py -H <HOST> -P <PORT>
```

To run the data generator:
```bash
export PYTHONPATH=$(pwd):${PYTHONPATH}
python stream_online_viewer/start_stream.py
```

To access the client viewer go
### Changelog
-------------------------

See file `CHANGES.rst`.

## Contact
-------------------------

For comments and requests, contact:
```
leonardo.hax@psi.ch
```

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
