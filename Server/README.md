# mbox_speaker_diarization

### 1. Description
This project contains scripts for a speaker diarization server intended to run in a Linux environment. 

The server and clientcommunicate with ZMQ ([pyzmq](https://github.com/zeromq/pyzmq)) protocol. Diarization is made with Google Cloud speech-to-text API.

This project is one of the sub-parts to Multimodal Learning Analytics Box (MBOX) which is a research project at Malmo University.


### 2. Installation
First make sure python3 is installed. 

Then make sure third-party libraries is installed:
- pyzmq
- pandas
- google-cloud-speech

