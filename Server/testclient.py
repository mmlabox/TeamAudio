import zmq
import base64

# Opens the recorded sound, 'output.wav' and encodes it
f = open("/home/robin_jf_andersson/mbox_speaker_diarization/audiofiles/Test7.wav", 'rb')
bytes = bytearray(f.read())
byte_wav = base64.b64encode(bytes)
f.close()
message = { 
    "channels":     4,
    "sample_rate":  16000,
    "audio_file": byte_wav,
}

context = zmq.Context()

# Socket to talk to server
socket = context.socket(zmq.PUSH)
socket.connect("tcp://0.0.0.0:8080")

print("Sending request...")
#socket.send(byte_wav)
socket.send_pyobj(message)

