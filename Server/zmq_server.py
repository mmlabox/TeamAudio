import diarization_service as ds
import zmq
import datetime
import base64
import pandas as pd
from influxdb import DataFrameClient
import config
import datetime

''' 
A server running constantly checking for incoming messages through ZMQ protocol and process the
message, sending the data to an influx Database. Currently we do not stream live words, meaning the
datetimeindex stored into the InfluxDB will not be correct. Whole conversation comes in one minute batch
This is something to be fixed with for instance several ZMQ workers (threads) that process sentences or maybe
10 second time periods at a time. The foundation is already set for creating the Dataframe, which then will
give a more accurate timestamp. Another option would also be to seperate zmq workers by speaker tag, so that
each speaker is processed by a worker and get a more accurate time-stamp.
'''

#ZMQ for receiving wav files to process
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://0.0.0.0:8080")




while True:
    print("waiting for incoming package from client...")
    recieved_file = socket.recv_pyobj()
    print("-----------\npackage recieved from client")

    auido_bytes = recieved_file["audio_file"]
    audio_channels = recieved_file["channels"]
    audio_sample_rate = recieved_file["sample_rate"]
    decode_string = base64.b64decode(auido_bytes)
    time = datetime.datetime.now()                  #for generating unique file names for the audiofile
    wav_file = open("audiofiles/%s.wav" % (time), "wb")
    wav_file.write(decode_string)
    wav_file.close()
    print("with file: ", wav_file.name, "\nchannels: ", audio_channels, " hertz: ", audio_sample_rate, "\n-----------")
    res = ds.speaker_diarization(wav_file.name, audio_channels, audio_sample_rate, 3)

    #df = pd.DataFrame.from_dict(res) this didnt work very well, do it manually below instead
    data = []
    for key in res:
        data.append([key, res[key]["number_of_words"], res[key]["words"], datetime.datetime.now()])
    
    columns = ["speaker", "wordcount", "wordlist", "date_time"]
    df = pd.DataFrame(data=data, columns=columns)
    datetime_series = pd.to_datetime(df['date_time'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df = df.set_index(datetime_index)
    df = df.drop("date_time", axis=1)

    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


    #Writing the collected data to influxDB
    client = DataFrameClient(
        host=config.host, 
        port=config.port, 
        database= config.database, 
        username=config.username, 
        password=config.password
    )
    client.write_points(df, config.measurement, batch_size=1000)

