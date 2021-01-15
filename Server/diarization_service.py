import os
from google.cloud import speech_v1p1beta1 as speech
import io

#Set env variable, because it resets every shell session
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/robin_jf_andersson/mbox_speaker_diarization/mbox1-28508a73fde1.json"

def speaker_diarization(audio_file, channels, sample_rate, nbr_of_persons):
    client = speech.SpeechClient()
    speech_file = audio_file

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=nbr_of_persons,
        audio_channel_count=channels,
        enable_separate_recognition_per_channel=True, #change this if respeaker is configured correctly
        model="video",
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    output_result = {}
    #saving each word with corresponding speaker tag into a dictionary of word lists
    for i in range(nbr_of_persons):
        word_counter = 0
        speaker_data = {}
        words = []
        for word_info in words_info:
            if(word_info.speaker_tag == (i+1)):
                words.append(word_info.word)
                word_counter += 1
        speaker_data["number_of_words"] = word_counter
        speaker_data["words"] = words
        output_result[(i+1)] = speaker_data

    #print(output_result)

    return output_result
   



#test
#diarization_service("audiofiles/Test7.wav")



    
    


