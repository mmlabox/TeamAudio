# THIS SCRIPT CONTAINS A FUNCTION 
# THAT SENDS THE AUDIO FILE TO
# THE SERVER.

import zmq

def send_audio(audio_info):
    context = zmq.Context()

    socket = context.socket(zmq.PUSH)
    # If you are not using a local server, replace localhost 
    # with your IP and the port 5556 with the actual port number.
    socket.connect("tcp://localhost:5556")
    socket.send_pyobj(audio_info)

    print("\nSent the audio information to the server.")
    
    # FOR LOCAL SERVER TEST, TRY THE 
    # CODE BELOW TO GET REPLY

    # message = socket.recv()
    # print("\nReceived reply --- " + str(message) + " ---")