# Stream online viewer

The goal of this task is to display a stream in a web client.

Lets imagine that the stream source is a camera that is sending live images of the beam in SwissFEL. 
In the stream, together with the raw image, there are also some calculated data and metadata the user might want to see.

The user is interested in live stream viewing and wants to use a web browser to do that.

## Backend

You have to create a Flask based Python web server that is capable of receiving a stream 
and displaying it to the user in his browser:

- One Flask web server is always receiving only 1 stream (the stream address should be a startup parameter for 
the web server). 
- Multiple clients can watch the stream on one web server (multiple web clients connected).
- The server should be always listening to the stream for messages and discard this messages if there are no clients to 
send the message to.
- Each client should start receiving images from the moment he connects onward 
(do not send old images that the server received before the client connected).

## Frontend

You have to create an HTML based web client to display the data sent from the backend:

- When a user opens the web page, it should automatically start receiving the latest data from the server.
- The web page should display to the user the image and metadata from the stream.
- You can use any frontend technology and library you want.

# Expected results
The expected outcomes of this task are:

- Git repository with a working solution compatible with the task description above.
- README with instructions on how to deploy, run and test your solution.
- Short summary of your solution (can be another Markdown file):
    - Briefly describe your architecture.
    - What are the drawbacks of your implementation?
    - Extra credits:
        - Can you estimate (or measure) the performance constraints (number of users, images per second etc.) 
        of your system? 
        - How can your implementation be improved?

# Instructions
- Install the needed dependencies (see chapter below).
- Based on the task description above, implement your solution in this repository.
    - Use stream_online_viewer/start_stream.py to generate a testing stream for your web server.
- **stream\_online\_viewer/start\_server.py** should be the entry point for your web server.
- Prepare the project documentation (replace this README).
- Prepare a short summary of your solution.
- Compress this repository (zip or tar.gz) and send it back over email.

We expect to be able to deploy, run and test your solution based on the instructions in your README.

You should work toward the solution of this task alone. If you have any questions or problems related to the libraries 
we use feel free to ask.

## Dependencies
We use Anaconda for packaging our libraries. If you are not familiar with Anaconda, have a look at their website: 

[https://anaconda.org/](https://anaconda.org/)

In order to use this repository, you will have to install the following conda packages:

- matplotlib
- numpy
- bsread

You can do this (on Linux) by running:
```bash
conda install -c paulscherrerinstitute bsread numpy matplotlib
```

We have our own Anaconda repository: 
[https://anaconda.org/paulscherrerinstitute/](https://anaconda.org/paulscherrerinstitute/)

When installing PSI libraries you have to specify that you want to install them from the PSI Anaconda repository 
(the "-c paulscherrerinstitute" flag in the command above).

### BSread
This is the protocol we use to transfer beam synchronous data at SwissFEL: 
[https://github.com/paulscherrerinstitute/bsread_python](https://github.com/paulscherrerinstitute/bsread_python)

You will not be able to access the real BSread stream from outside of PSI. This repository has a stream generator you 
can use to simulate camera images and metadata you will later display to the clients. The generator is located in 
**stream\_online\_viewer/start\_stream.py** and can be run from the ROOT of this repository:

```bash
export PYTHONPATH=$(PWD):${PYTHONPATH}
python stream_online_viewer/start_stream.py
```

To stop the stream press **CTRL + C**.

An example on how to receive the stream can be seen in the **tests/test\_stream.py** unit test. 
Additional documentation and specifications can be found on the Github page of the library (referenced above).