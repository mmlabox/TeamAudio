# THIS CODE HAS ONLY BEEN USED FOR
# LOCAL SERVER TO TEST IF ZMQ
# WORKS PROPERLY

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

while True:

    # Waits for request from client
    # and runs when the audio information
    # has been sended from client.py
    message = socket.recv_pyobj()
    print("Received audio:")

    # To access from the pyobj, you can do 
    # message['channels'] for example.

    time.sleep(1)

    # Sending reply back to the client
    socket.send_string("Successfully sended!")