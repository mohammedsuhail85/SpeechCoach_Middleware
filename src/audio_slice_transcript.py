import os
import glob
from pydub import AudioSegment
import requests
from flask import jsonify

FILE_PATH = "/home/suhail/Desktop/SpeechEmotionAnalyzer/temp/"


def get_transcript(file_path, session):
    try:
        sound = AudioSegment.from_file(file_path)

        duration = sound.duration_seconds
        slicing_time = 10
        print(duration)

        count = (duration // slicing_time) + 1
        count = int(count)
        print(count)

        list_audio = []

        for x in range(0, count):
            start = x*slicing_time*1000
            end = (x+1)*slicing_time*1000
            segment = sound[start:end]
            audio_file_name = FILE_PATH + "seg"+str(x)+".wav"
            list_audio.append(audio_file_name)
            segment.set_channels(1).set_frame_rate(16000).export(audio_file_name, format="wav")

        print("saved")

        url_transcript = "http://127.0.0.1:6000/audio/process"

        response_list = []

        for x in list_audio:
            print(x)

            multipart = {'file': ('sample.wav', open(x, 'rb'), 'audio/x-wav', {'Expires': '0'})}
            print("Making Request")

            response = requests.post(url_transcript, files=multipart)
            if response.status_code == 200:
                response_list.append(response.json())

        print("Request completed")
        # for x in response_list:
        #     print(x)
        return response_list
    except ConnectionRefusedError:
        return jsonify({
            "Error": "Speech Emotion Component Connection Refused"
        })
    # except Exception as ex:
    #     ex.with_traceback()